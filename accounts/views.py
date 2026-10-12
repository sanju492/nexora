
from django.contrib import messages
from django.contrib.auth import (
    authenticate, login, logout, get_user_model,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from employees.models import EmployeeProfile
from attendance.models import Attendance

User = get_user_model()


def home(request):
    return render(request, "home.html")


def is_manager(request):
    return (
        request.user.is_authenticated
        and getattr(request.user, "role", None) == "manager"
    )


# MANAGER LOGIN
def manager_login(request):
    if request.user.is_authenticated:
        if is_manager(request):
            request.session["nexora_manager"] = True
            return redirect("manager_dashboard")
        logout(request)

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request, username=username, password=password
        )

        if (
            user is not None
            and getattr(user, "role", None) == "manager"
            and user.is_active
        ):
            login(request, user)
            request.session["nexora_manager"] = True
            request.session.modified = True
            return redirect("manager_dashboard")

        messages.error(
            request,
            "Invalid manager username or password, or account inactive.",
        )
        return redirect("manager_login")

    return render(request, "accounts/manager_login.html")


# MANAGER DASHBOARD
@login_required
def manager_dashboard(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    context = {
        "employee_count": User.objects.filter(role="employee").count(),
        "hr_count": User.objects.filter(role="hr").count(),
        "pending_employees": User.objects.filter(
            role="employee", is_active=False
        ).count(),
        "pending_hr": User.objects.filter(
            role="hr", is_active=False
        ).count(),
    }
    return render(request, "accounts/manager_dashboard.html", context)


# EMPLOYEE LOGIN
def employee_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(
            request, username=username, password=password
        )

        if user is not None and getattr(user, "role", None) == "employee":
            if not user.is_active:
                messages.error(
                    request,
                    "Your account is awaiting manager approval.",
                )
                return redirect("employee_login")

            login(request, user)
            return redirect("employee_dashboard")

        messages.error(request, "Invalid employee login details.")
        return redirect("employee_login")

    return render(request, "accounts/employee_login.html")


# HR LOGIN
def hr_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(
            request, username=username, password=password
        )

        if user is not None and getattr(user, "role", None) == "hr":
            if not user.is_active:
                messages.error(
                    request,
                    "Your account is awaiting manager approval.",
                )
                return redirect("hr_login")

            login(request, user)
            return redirect("hr_dashboard")

        messages.error(request, "Invalid HR login details.")
        return redirect("hr_login")

    return render(request, "accounts/hr_login.html")


# EMPLOYEE REGISTRATION
def employee_register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not all([username, email, password, confirm_password]):
            messages.error(request, "Please fill in all required fields.")
            return redirect("employee_register")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("employee_register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("employee_register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("employee_register")

        User.objects.create_user(
            username=username, email=email, password=password,
            role="employee", is_active=False,
        )
        messages.success(
            request,
            "Registration submitted. Please wait for manager approval.",
        )
        return redirect("employee_login")

    return render(request, "accounts/employee_register.html")


# HR REGISTRATION
def hr_register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not all([username, email, password, confirm_password]):
            messages.error(request, "Please fill in all required fields.")
            return redirect("hr_register")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("hr_register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("hr_register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("hr_register")

        User.objects.create_user(
            username=username, email=email, password=password,
            role="hr", is_active=False,
        )
        messages.success(
            request,
            "HR registration submitted. Please wait for manager approval.",
        )
        return redirect("hr_login")

    return render(request, "accounts/hr_register.html")


# MANAGER TEAM / APPROVAL REDIRECTS
@login_required
def pending_employees(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")
    return redirect("manager_team")


@login_required
def employee_approvals(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")
    return redirect("manager_team")


@login_required
def pending_hr(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")
    return redirect("manager_team")


@login_required
def hr_approvals(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")
    return redirect("manager_team")


# APPROVE / REJECT EMPLOYEE
@login_required
@require_POST
def approve_employee(request, user_id):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    employee = get_object_or_404(
        User, id=user_id, role="employee", is_active=False
    )
    employee.is_active = True
    employee.save(update_fields=["is_active"])
    messages.success(request, "Employee account approved.")
    return redirect("manager_team")


@login_required
@require_POST
def reject_employee(request, user_id):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    employee = get_object_or_404(
        User, id=user_id, role="employee", is_active=False
    )
    employee.delete()
    messages.success(request, "Pending employee registration rejected.")
    return redirect("manager_team")


# APPROVE / REJECT HR
@login_required
@require_POST
def approve_hr(request, user_id):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    hr_user = get_object_or_404(
        User, id=user_id, role="hr", is_active=False
    )
    hr_user.is_active = True
    hr_user.save(update_fields=["is_active"])
    messages.success(request, "HR account approved.")
    return redirect("manager_team")


@login_required
@require_POST
def reject_hr(request, user_id):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    hr_user = get_object_or_404(
        User, id=user_id, role="hr", is_active=False
    )
    hr_user.delete()
    messages.success(request, "Pending HR registration rejected.")
    return redirect("manager_team")


# EMPLOYEE DASHBOARD
@login_required
def employee_dashboard(request):
    if getattr(request.user, "role", None) != "employee":
        return HttpResponseForbidden("Employee access only.")

    employee = EmployeeProfile.objects.filter(user=request.user).first()
    return render(
        request, "accounts/employee_dashboard.html",
        {"employee": employee},
    )


# HR DASHBOARD
@login_required
def hr_dashboard(request):
    if getattr(request.user, "role", None) != "hr":
        return HttpResponseForbidden("HR access only.")

    hr_profile = EmployeeProfile.objects.filter(user=request.user).first()
    return render(
        request, "accounts/hr_dashboard.html",
        {"employee": hr_profile},
    )


# MANAGER ATTENDANCE
@login_required
def manager_attendance(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    attendance_records = Attendance.objects.select_related(
        "employee", "employee__user"
    ).order_by("-id")

    return render(
        request, "accounts/manager_attendance.html",
        {"attendance_records": attendance_records},
    )


# LOGOUT
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("home")


# MANAGER TEAM
@login_required
def manager_team(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    employees = EmployeeProfile.objects.select_related("user").filter(
        user__role="employee", user__is_active=True
    ).order_by("user__username")

    context = {
        "employees": employees,
        "total_hr": User.objects.filter(role="hr").count(),
        "approved_hr_count": User.objects.filter(
            role="hr", is_active=True
        ).count(),
        "rejected_hr_count": 0,
        "total_employees": User.objects.filter(role="employee").count(),
        "approved_employees_count": User.objects.filter(
            role="employee", is_active=True
        ).count(),
        "rejected_employees_count": 0,
    }
    return render(request, "accounts/manager_team.html", context)


@login_required
def manager_team_employees(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    employees = EmployeeProfile.objects.select_related("user").filter(
        user__role="employee", user__is_active=True
    ).order_by("user__username")

    return render(
        request, "accounts/manager_team.html", {"employees": employees}
    )


@login_required
def manager_team_hr(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    hr_users = User.objects.filter(
        role="hr", is_active=True
    ).order_by("username")
    return render(
        request, "accounts/manager_team.html", {"hr_users": hr_users}
    )


@login_required
def manager_approved_hr(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    hr_users = User.objects.filter(
        role="hr", is_active=True
    ).order_by("username")
    return render(
        request, "accounts/manager_team.html", {"hr_users": hr_users}
    )


@login_required
def manager_rejected_hr(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    return render(
        request, "accounts/manager_team.html",
        {"hr_users": User.objects.none()},
    )


@login_required
def manager_approved_employees(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    employees = EmployeeProfile.objects.select_related("user").filter(
        user__role="employee", user__is_active=True
    ).order_by("user__username")

    return render(
        request, "accounts/manager_team.html", {"employees": employees}
    )


@login_required
def manager_rejected_employees(request):
    if not is_manager(request):
        return HttpResponseForbidden("Manager access only.")

    return render(
        request, "accounts/manager_team.html",
        {"employees": EmployeeProfile.objects.none()},
    )
