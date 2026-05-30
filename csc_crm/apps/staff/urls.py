from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_page, name='attendance'),

    path('staff-checkin/', views.staff_checkin, name='staff_checkin'),

]