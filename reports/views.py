
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from employees.models import EmployeeProfile
from attendance.models import Attendance
from leaves.models import Leave
from payroll.models import Payroll

from .models import Report


User = get_user_model()


def allowed_receiver_roles(role):
    """Define which roles can send reports to which recipients."""

    role = (role or "").lower()

    permissions = {
        "employee": ["hr"],
        "hr": ["employee", "manager"],
        "manager": ["hr"],
    }

    return permissions.get(role, [])


@login_required
def reports_dashboard(request):
    role = (getattr(request.user, "role", "") or "").lower()

    received_reports = Report.objects.filter(
        receiver=request.user
    ).select_related("sender")

    sent_reports = Report.objects.filter(
        sender=request.user
    ).select_related("receiver")

    context = {
        "received_reports": received_reports[:10],
        "sent_reports": sent_reports[:10],
        "received_count": received_reports.count(),
        "sent_count": sent_reports.count(),
        "unread_count": received_reports.filter(
            status="unread"
        ).count(),
        "user_role": role,
    }

    # Employee reports dashboard
    if role == "employee":
        return render(
            request,
            "reports/employee_dashboard.html",
            context,
        )

    # HR reports dashboard
    elif role == "hr":
        context.update({
            "total_employees": EmployeeProfile.objects.count(),
            "total_attendance": Attendance.objects.count(),
            "total_leave_requests": Leave.objects.count(),
            "total_payroll_records": Payroll.objects.count(),
        })

        return render(
            request,
            "reports/dashboard.html",
            context,
        )

    # Manager reports dashboard
    elif role == "manager":
        return render(
            request,
            "reports/manager_dashboard.html",
            context,
        )

    return HttpResponseForbidden(
        "You are not authorized to access the reports dashboard."
    )


@login_required
def send_report(request):
    role = (getattr(request.user, "role", "") or "").lower()

    permitted_roles = allowed_receiver_roles(role)

    recipients = User.objects.filter(
        role__in=permitted_roles,
        is_active=True,
    ).exclude(
        pk=request.user.pk
    ).order_by("username")

    if request.method == "POST":
        receiver_id = request.POST.get("receiver")
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if not receiver_id or not subject or not message:
            return render(
                request,
                "reports/send_report.html",
                {
                    "recipients": recipients,
                    "error": "Please complete all fields.",
                },
            )

        receiver = get_object_or_404(
            recipients,
            pk=receiver_id,
        )

        Report.objects.create(
            sender=request.user,
            receiver=receiver,
            subject=subject,
            message=message,
        )

        return redirect("reports:reports_dashboard")

    return render(
        request,
        "reports/send_report.html",
        {
            "recipients": recipients,
        },
    )


@login_required
def inbox_reports(request):
    reports = Report.objects.filter(
        receiver=request.user
    ).select_related(
        "sender",
        "receiver",
    )

    return render(
        request,
        "reports/inbox.html",
        {
            "reports": reports,
        },
    )


@login_required
def sent_reports(request):
    reports = Report.objects.filter(
        sender=request.user
    ).select_related(
        "sender",
        "receiver",
    )

    return render(
        request,
        "reports/sent.html",
        {
            "reports": reports,
        },
    )


@login_required
def report_detail(request, report_id):
    report = get_object_or_404(
        Report.objects.select_related(
            "sender",
            "receiver",
        ),
        pk=report_id,
    )

    # Only the sender or receiver can view this report.
    if request.user.pk not in (
        report.sender_id,
        report.receiver_id,
    ):
        return HttpResponseForbidden(
            "You are not allowed to view this report."
        )

    # Mark the report as read when the receiver opens it.
    if (
        request.user.pk == report.receiver_id
        and report.status == "unread"
    ):
        report.status = "read"
        report.save(update_fields=["status"])

    return render(
        request,
        "reports/report_detail.html",
        {
            "report": report,
        },
    )
