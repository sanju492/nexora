from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import EmployeeProfile


@login_required
def hr_employee_list(request):
    if getattr(request.user, "role", "") != "hr":
        messages.error(request, "HR access only.")
        return redirect("home")

    employees = (
        EmployeeProfile.objects
        .select_related("user", "department")
        .order_by("employee_id")
    )

    context = {
        "employees": employees,
    }

    return render(
        request,
        "employees/hr_employee_list.html",
        context,
    )