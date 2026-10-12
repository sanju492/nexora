
from django.urls import path
from . import views

app_name = "payroll"

urlpatterns = [
    path(
        "employee/",
        views.employee_payroll,
        name="employee_payroll",
    ),
    path(
        "hr/",
        views.hr_payroll,
        name="hr_payroll",
    ),
    path(
        "manager/",
        views.manager_payroll,
        name="manager_payroll",
    ),
]
