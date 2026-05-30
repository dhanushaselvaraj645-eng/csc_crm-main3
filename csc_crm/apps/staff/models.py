from django.db import models
from django.utils import timezone


# STAFF MODEL

class Staff(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    department = models.CharField(max_length=100)

    def __str__(self):

        return self.name




# ATTENDANCE MODEL

class Attendance(models.Model):


    STATUS_CHOICES = (

        ('Present', 'Present'),

        ('Absent', 'Absent'),

        ('Leave', 'Leave'),

        ('Late', 'Late'),

    )


    # STAFF CONNECT

    staff = models.ForeignKey(

        Staff,

        on_delete=models.CASCADE,

        related_name='attendances',

        null=True,

        blank=True

    )


    # DATE

    date = models.DateField(default=timezone.now)


    # CHECK IN

    check_in = models.DateTimeField(null=True,blank=True)


    # CHECK OUT

    check_out = models.DateTimeField(null=True,blank=True)


    # TOTAL HOURS

    total_hours = models.CharField(max_length=20, null=True,blank=True)


    # STATUS

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Absent')



    # SAVE METHOD

    def save(self, *args, **kwargs):


        # TOTAL HOURS

        if self.check_in and self.check_out:


            total = self.check_out - self.check_in


            hours = total.seconds // 3600


            minutes = (
                total.seconds % 3600
            ) // 60


            self.total_hours = (
                f"{hours}h {minutes}m"
            )


        super().save(*args, **kwargs)




    def __str__(self):


        if self.staff:

            return f"{self.staff.name} - {self.date}"


        return f"{self.date}"




    class Meta:

        db_table = "staff_attendance"