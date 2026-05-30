from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.utils import timezone

from .models import Attendance
from .models import Staff

from datetime import datetime




# ATTENDANCE PAGE

def attendance_page(request):


    # FILTER VALUES

    date = request.GET.get('date')

    month = request.GET.get('month')

    year = request.GET.get('year')



    # ALL DATA

    attendance_data = Attendance.objects.all().order_by('-date')



    # DATE FILTER

    if date:

        attendance_data = attendance_data.filter(date=date)



    # MONTH FILTER

    if month:

        attendance_data = attendance_data.filter(date__month=month)



    # YEAR FILTER

    if year:

        attendance_data = attendance_data.filter(date__year=year)



    # TOTAL DAYS

    total_working_days = attendance_data.count()



    # PRESENT

    present_days = attendance_data.filter(status='Present').count()



    # ABSENT

    absent_days = attendance_data.filter(status='Absent').count()



    # LEAVE

    leave_days = attendance_data.filter(status='Leave').count()



    # LATE

    late_days = attendance_data.filter(status='Late').count()



    # ATTENDANCE %

    if total_working_days > 0:

        attendance_percentage = int(

            (present_days + late_days)

            / total_working_days * 100

        )

    else:

        attendance_percentage = 0



    # TODAY STATUS

    today = timezone.localdate()



    today_attendance = Attendance.objects.filter(date=today).order_by('-id').first()



    if today_attendance:

        today_status = today_attendance.status

    else:

        today_status = 'Absent'



    context = {

        'attendance_data': attendance_data,

        'total_working_days': total_working_days,

        'present_days': present_days,

        'absent_days': absent_days,

        'leave_days': leave_days,

        'late_days': late_days,

        'attendance_percentage': attendance_percentage,

        'today_status': today_status,

        'today_attendance': today_attendance,

    }



    return render(

        request,

        'staff/attendance.html',

        context

    )


# STAFF ATTENDANCE ENTRY


def staff_checkin(request):


    if request.method == 'POST':


        # STAFF NAME

        staff_name = request.POST.get('staff_name')


        # BUTTON ACTION

        action = request.POST.get('action')


        # FIND STAFF

        staff = Staff.objects.filter(name=staff_name).first()


        if not staff:

            return redirect('staff_checkin')


        # TODAY DATE

        today = timezone.localdate()


        # CURRENT TIME

        current_time = timezone.localtime(timezone.now())


        # FIND TODAY ATTENDANCE

        attendance = Attendance.objects.filter(staff=staff, date=today).first()


        # CREATE ENTRY

        if not attendance:

            attendance = Attendance(staff=staff,date=today)


        # CHECK IN

        if action == 'checkin':


            attendance.check_in = current_time

            office_time = datetime.strptime(
                "09:15",
                "%H:%M"
            ).time()


            if current_time.time() > office_time:

                attendance.status = 'Late'

            else:

                attendance.status = 'Present'
        

        # CHECK OUT

        elif action == 'checkout':


            attendance.check_out = current_time
        # leave
        elif action == 'leave':

            attendance.status = 'Leave'
            attendance.check_in = None
            attendance.check_out = None
            attendance.total_hours = None


         #absent
        elif action == 'absent':

            attendance.status = 'Absent'

            attendance.check_in = None

            attendance.check_out = None

            attendance.total_hours = None
        attendance.save()


        return redirect('attendance')


    return render(

        request,

        'staff/staff_checkin.html'

    )






