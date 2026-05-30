from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_page, name='attendance'),

    path('staff-checkin/', views.staff_checkin, name='staff_checkin'),

    path('delete/<int:id>/', views.delete_attendance, name='delete_attendance'),
]