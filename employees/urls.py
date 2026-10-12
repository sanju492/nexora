from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path("hr/", views.hr_employee_list, name="hr_employee_list"),
]