
from django.urls import path
from . import views

app_name = "leaves"

urlpatterns = [
    # Employee Leave
    path(
        "",
        views.employee_leave_management,
        name="employee_leave_management",
    ),

    # HR Leave
    path(
        "hr/",
        views.hr_leave_requests,
        name="hr_leave_requests",
    ),

    # Manager - Employee Leave Requests
    path(
        "manager/",
        views.manager_leave_requests,
        name="manager_leave_requests",
    ),
    path(
        "manager/<int:leave_id>/approve/",
        views.approve_leave,
        name="approve_leave",
    ),
    path(
        "manager/<int:leave_id>/reject/",
        views.reject_leave,
        name="reject_leave",
    ),

    # Manager - HR Leave Requests
    path(
        "manager/hr/",
        views.manager_hr_leave_requests,
        name="manager_hr_leave_requests",
    ),
    path(
        "manager/hr/<int:leave_id>/approve/",
        views.approve_hr_leave,
        name="approve_hr_leave",
    ),
    path(
        "manager/hr/<int:leave_id>/reject/",
        views.reject_hr_leave,
        name="reject_hr_leave",
    ),
]
