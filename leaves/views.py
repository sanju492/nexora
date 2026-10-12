
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from employees.models import EmployeeProfile
from .models import Leave


# ============================================================
# EMPLOYEE LEAVE MANAGEMENT
# ============================================================

@login_required
def employee_leave_management(request):
    employee = EmployeeProfile.objects.filter(
        user=request.user
    ).first()

    if not employee:
        messages.error(request, "Employee profile not found.")
        return redirect("employee_dashboard")

    if request.method == "POST":
        leave_type = request.POST.get("leave_type")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason", "").strip()

        if not all([leave_type, start_date, end_date, reason]):
            messages.error(request, "Please fill all fields.")
            return redirect("employee_leave_management")

        if end_date < start_date:
            messages.error(
                request,
                "To Date cannot be before From Date."
            )
            return redirect("employee_leave_management")

        Leave.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status="pending",
        )

        messages.success(
            request,
            "Leave application submitted successfully."
        )
        return redirect("employee_leave_management")

    leave_requests = Leave.objects.filter(
        employee=employee
    ).order_by("-applied_on")

    return render(
        request,
        "leaves/employee_leave_management.html",
        {
            "employee": employee,
            "leave_requests": leave_requests,
        },
    )


# ============================================================
# HR LEAVE MANAGEMENT
# ============================================================

@login_required
def hr_leave_requests(request):
    if request.user.role != "hr":
        messages.error(request, "HR access required.")
        return redirect("home")

    hr = EmployeeProfile.objects.filter(
        user=request.user
    ).first()

    if not hr:
        messages.error(request, "HR profile not found.")
        return redirect("hr_dashboard")

    if request.method == "POST":
        leave_type = request.POST.get("leave_type")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason", "").strip()

        if not all([leave_type, start_date, end_date, reason]):
            messages.error(request, "Please fill all fields.")
            return redirect("hr_leave_requests")

        if end_date < start_date:
            messages.error(
                request,
                "To Date cannot be before From Date."
            )
            return redirect("hr_leave_requests")

        Leave.objects.create(
            employee=hr,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status="pending",
        )

        messages.success(
            request,
            "Leave request submitted successfully."
        )
        return redirect("hr_leave_requests")

    leave_requests = Leave.objects.filter(
        employee=hr
    ).order_by("-applied_on")

    return render(
        request,
        "leaves/hr_leave_requests.html",
        {
            "hr": hr,
            "leave_requests": leave_requests,
        },
    )


# ============================================================
# MANAGER ACCESS HELPER
# ============================================================

def manager_session_valid(request):
    return request.session.get("nexora_manager", False)


# ============================================================
# MANAGER - EMPLOYEE LEAVE REQUESTS
# ============================================================

def manager_leave_requests(request):
    if not manager_session_valid(request):
        return redirect("manager_login")

    leave_requests = Leave.objects.select_related(
        "employee",
        "employee__user",
        "employee__department",
    ).filter(
        employee__user__role="employee"
    ).order_by("-applied_on")

    context = {
        "leave_requests": leave_requests,
        "pending_count": leave_requests.filter(status="pending").count(),
        "approved_count": leave_requests.filter(status="approved").count(),
        "rejected_count": leave_requests.filter(status="rejected").count(),
        "total_count": leave_requests.count(),
    }

    return render(
        request,
        "leaves/manager_leave_requests.html",
        context,
    )


# ============================================================
# MANAGER - HR LEAVE REQUESTS
# ============================================================

def manager_hr_leave_requests(request):
    if not manager_session_valid(request):
        return redirect("manager_login")

    leave_requests = Leave.objects.select_related(
        "employee",
        "employee__user",
        "employee__department",
    ).filter(
        employee__user__role="hr"
    ).order_by("-applied_on")

    context = {
        "leave_requests": leave_requests,
        "pending_count": leave_requests.filter(status="pending").count(),
        "approved_count": leave_requests.filter(status="approved").count(),
        "rejected_count": leave_requests.filter(status="rejected").count(),
        "total_count": leave_requests.count(),
    }

    return render(
        request,
        "leaves/manager_hr_leave_requests.html",
        context,
    )


# ============================================================
# MANAGER - UPDATE LEAVE STATUS HELPER
# ============================================================

def update_leave_status(request, leave_id, role, status):
    if not manager_session_valid(request):
        return redirect("manager_login")

    if request.method != "POST":
        messages.error(request, "Use the form to update leave status.")
        return redirect(
            "manager_hr_leave_requests"
            if role == "hr"
            else "manager_leave_requests"
        )

    leave = get_object_or_404(
        Leave,
        id=leave_id,
        employee__user__role=role,
    )

    if status not in ("approved", "rejected"):
        messages.error(request, "Invalid leave status.")
    else:
        leave.status = status
        leave.save(update_fields=["status"])
        messages.success(
            request,
            f"{role.upper()} leave request {status} successfully."
        )

    return redirect(
        "manager_hr_leave_requests"
        if role == "hr"
        else "manager_leave_requests"
    )


# ============================================================
# MANAGER - APPROVE / REJECT EMPLOYEE LEAVE
# ============================================================

def approve_leave(request, leave_id):
    return update_leave_status(
        request, leave_id, "employee", "approved"
    )


def reject_leave(request, leave_id):
    return update_leave_status(
        request, leave_id, "employee", "rejected"
    )


# ============================================================
# MANAGER - APPROVE / REJECT HR LEAVE
# ============================================================

def approve_hr_leave(request, leave_id):
    return update_leave_status(
        request, leave_id, "hr", "approved"
    )


def reject_hr_leave(request, leave_id):
    return update_leave_status(
        request, leave_id, "hr", "rejected"
    )
