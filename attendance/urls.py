from django.urls import path
from . import views


urlpatterns = [

    # Employee Attendance
    path(
        '',
        views.employee_attendance,
        name='employee_attendance'
    ),

    path(
        'office/check-in/',
        views.office_check_in,
        name='office_check_in'
    ),

    path(
        'office/check-out/',
        views.office_check_out,
        name='office_check_out'
    ),

    path(
        'wfh/check-in/',
        views.wfh_check_in,
        name='wfh_check_in'
    ),

    path(
        'wfh/check-out/',
        views.wfh_check_out,
        name='wfh_check_out'
    ),


    # HR Attendance
    path(
        'hr/',
        views.hr_attendance,
        name='hr_attendance'
    ),

    path(
        'hr/office/check-in/',
        views.hr_office_check_in,
        name='hr_office_check_in'
    ),

    path(
        'hr/office/check-out/',
        views.hr_office_check_out,
        name='hr_office_check_out'
    ),

    path(
        'hr/wfh/check-in/',
        views.hr_wfh_check_in,
        name='hr_wfh_check_in'
    ),

    path(
        'hr/wfh/check-out/',
        views.hr_wfh_check_out,
        name='hr_wfh_check_out'
    ),
]