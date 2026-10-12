
from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path("", views.home, name="home"),

    # EMPLOYEE
    path("employee/login/", views.employee_login, name="employee_login"),
    path("employee/register/", views.employee_register, name="employee_register"),
    path("employee/dashboard/", views.employee_dashboard, name="employee_dashboard"),

    # HR
    path("hr/login/", views.hr_login, name="hr_login"),
    path("hr/register/", views.hr_register, name="hr_register"),
    path("hr/dashboard/", views.hr_dashboard, name="hr_dashboard"),

    # MANAGER
    path("manager/login/", views.manager_login, name="manager_login"),
    path("manager/dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("manager/attendance/", views.manager_attendance, name="manager_attendance"),

    # EMPLOYEE REGISTRATION APPROVALS
    path("manager/employee-registrations/", views.employee_approvals, name="employee_approvals"),
    path("manager/approve/<int:employee_id>/", views.approve_employee, name="approve_employee"),
    path("manager/reject/<int:employee_id>/", views.reject_employee, name="reject_employee"),

    # HR REGISTRATION APPROVALS
    path("manager/hr-registrations/", views.hr_approvals, name="hr_approvals"),
    path("manager/approve-hr/<int:employee_id>/", views.approve_hr, name="approve_hr"),
    path("manager/reject-hr/<int:employee_id>/", views.reject_hr, name="reject_hr"),

    # MANAGER TEAM
    path("manager/team/", views.manager_team, name="manager_team"),
    path("manager/team/employees/", views.manager_team_employees, name="manager_team_employees"),
    path("manager/team/hr/", views.manager_team_hr, name="manager_team_hr"),

    # APPROVED / REJECTED HR
    path("manager/team/hr/approved/", views.manager_approved_hr, name="manager_approved_hr"),
    path("manager/team/hr/rejected/", views.manager_rejected_hr, name="manager_rejected_hr"),

    # APPROVED / REJECTED EMPLOYEES
    path("manager/team/employees/approved/", views.manager_approved_employees, name="manager_approved_employees"),
    path("manager/team/employees/rejected/", views.manager_rejected_employees, name="manager_rejected_employees"),
]
