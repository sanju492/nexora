
from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.dateparse import parse_date

from employees.models import EmployeeProfile
from payroll.models import Payroll


def get_user_role(user):
    return str(getattr(user, "role", "") or "").strip().lower()


# EMPLOYEE PAYROLL
@login_required
def employee_payroll(request):
    role = get_user_role(request.user)

    if role not in ("employee", "hr"):
        return HttpResponseForbidden(
            "Only employees and HR users can access this page."
        )

    employee = EmployeeProfile.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return render(
            request,
            "payroll/employee_payroll.html",
            {
                "employee": None,
                "payroll_records": [],
                "total_paid": Decimal("0.00"),
                "pending_total": Decimal("0.00"),
                "error_message": "Employee profile not found.",
            },
        )

    payroll_records = Payroll.objects.filter(
        employee=employee
    ).order_by("-month")

    total_paid = sum(
        (
            record.net_salary
            for record in payroll_records
            if record.payment_status == "paid"
        ),
        start=Decimal("0.00"),
    )

    pending_total = sum(
        (
            record.net_salary
            for record in payroll_records
            if record.payment_status == "pending"
        ),
        start=Decimal("0.00"),
    )

    return render(
        request,
        "payroll/employee_payroll.html",
        {
            "employee": employee,
            "payroll_records": payroll_records,
            "total_paid": total_paid,
            "pending_total": pending_total,
        },
    )


# HR PAYROLL
@login_required
def hr_payroll(request):
    if get_user_role(request.user) != "hr":
        return HttpResponseForbidden(
            "Only HR users can access this page."
        )

    employee = EmployeeProfile.objects.filter(
        user=request.user
    ).first()

    payroll_records = Payroll.objects.none()

    if employee:
        payroll_records = Payroll.objects.filter(
            employee=employee
        ).order_by("-month")

    total_paid = sum(
        (
            record.net_salary
            for record in payroll_records
            if record.payment_status == "paid"
        ),
        start=Decimal("0.00"),
    )

    pending_total = sum(
        (
            record.net_salary
            for record in payroll_records
            if record.payment_status == "pending"
        ),
        start=Decimal("0.00"),
    )

    return render(
        request,
        "payroll/hr_payroll.html",
        {
            "employee": employee,
            "payroll_records": payroll_records,
            "total_paid": total_paid,
            "pending_total": pending_total,
        },
    )


# MANAGER PAYROLL
@login_required
def manager_payroll(request):
    role = get_user_role(request.user)

    if role != "manager":
        return HttpResponseForbidden(
            f"Only managers can manage payroll. "
            f"Your account role is: {role or 'not set'}"
        )

    error_message = None

    if request.method == "POST":

        # UPDATE AN EXISTING PAYROLL STATUS
        if request.POST.get("action") == "update_status":
            payroll_id = request.POST.get("payroll_id", "").strip()
            new_status = request.POST.get(
                "payment_status", ""
            ).strip().lower()

            if new_status not in ("pending", "paid"):
                messages.error(request, "Select a valid payment status.")
                return redirect("payroll:manager_payroll")

            try:
                with transaction.atomic():
                    payroll = Payroll.objects.select_for_update().get(
                        pk=payroll_id
                    )

                    payroll.payment_status = new_status

                    if new_status == "paid":
                        if payroll.paid_on is None:
                            payroll.paid_on = timezone.localdate()
                    else:
                        payroll.paid_on = None

                    payroll.save(
                        update_fields=["payment_status", "paid_on"]
                    )

                messages.success(
                    request,
                    f"Payroll status updated to "
                    f"{payroll.get_payment_status_display()}."
                )

            except (Payroll.DoesNotExist, ValueError):
                messages.error(
                    request,
                    "Payroll record not found. Refresh the page and try again."
                )

            return redirect("payroll:manager_payroll")

        # CREATE A NEW PAYROLL
        try:
            employee_id = request.POST.get(
                "employee", ""
            ).strip()

            month_value = request.POST.get(
                "month", ""
            ).strip()

            if not employee_id or not month_value:
                raise ValueError(
                    "Select an employee and payroll month."
                )

            month = parse_date(month_value + "-01")

            if month is None:
                raise ValueError("Select a valid payroll month.")

            if month > date.today().replace(day=1):
                raise ValueError(
                    "Future payroll months are not allowed."
                )

            employee = EmployeeProfile.objects.get(
                pk=employee_id,
                user__role__in=["employee", "hr"],
            )

            basic_value = request.POST.get(
                "basic_salary", ""
            ).strip()

            allowance_value = request.POST.get(
                "allowances", "0"
            ).strip()

            deduction_value = request.POST.get(
                "deductions", "0"
            ).strip()

            if not basic_value or not allowance_value or not deduction_value:
                raise ValueError("Enter all salary amounts.")

            basic_salary = Decimal(basic_value)
            allowances = Decimal(allowance_value)
            deductions = Decimal(deduction_value)

            amounts = (
                basic_salary,
                allowances,
                deductions,
            )

            if not all(amount.is_finite() for amount in amounts):
                raise ValueError("Enter valid salary amounts.")

            if any(amount < 0 for amount in amounts):
                raise ValueError(
                    "Salary amounts cannot be negative."
                )

            maximum_amount = Decimal("99999999.99")

            if any(amount > maximum_amount for amount in amounts):
                raise ValueError("Salary amount is too large.")

            net_salary = basic_salary + allowances - deductions

            if net_salary < 0:
                raise ValueError(
                    "Deductions cannot exceed salary plus allowances."
                )

            with transaction.atomic():
                if Payroll.objects.filter(
                    employee=employee,
                    month=month,
                ).exists():
                    raise ValueError(
                        "Payroll already exists for this employee "
                        "and month. Update the existing record instead."
                    )

                # New payroll always starts as Pending.
                # Use Update Status after salary is actually paid.
                Payroll.objects.create(
                    employee=employee,
                    month=month,
                    basic_salary=basic_salary,
                    allowances=allowances,
                    deductions=deductions,
                    net_salary=net_salary,
                    payment_status="pending",
                )

            messages.success(
                request,
                "Payroll created successfully. Payment status: Pending."
            )

            return redirect("payroll:manager_payroll")

        except EmployeeProfile.DoesNotExist:
            error_message = "Selected employee or HR profile not found."

        except (ValueError, InvalidOperation):
            error_message = (
                "Check the employee, month and salary amounts. "
                "If payroll already exists for that month, "
                "update the existing record instead."
            )

        except IntegrityError:
            error_message = (
                "Payroll could not be saved. "
                "A duplicate payroll record may already exist."
            )

    # LOAD EMPLOYEE AND HR PAYROLL HISTORY
    profiles = EmployeeProfile.objects.filter(
        user__role__in=["employee", "hr"]
    ).select_related(
        "user",
        "department",
    ).order_by("employee_id")

    today = date.today()
    employee_data = []
    hr_data = []

    for profile in profiles:
        joining_date = profile.joining_date
        experience_years = 0

        if joining_date:
            experience_years = (
                today.year
                - joining_date.year
                - (
                    (today.month, today.day)
                    < (joining_date.month, joining_date.day)
                )
            )

        history = list(
            Payroll.objects.filter(
                employee=profile
            ).order_by("-month")
        )

        person = {
            "employee": profile,
            "experience_years": experience_years,
            "history": history,
            "latest_payroll": history[0] if history else None,
        }

        if get_user_role(profile.user) == "hr":
            hr_data.append(person)
        else:
            employee_data.append(person)

    payroll_count = Payroll.objects.count()

    return render(
        request,
        "payroll/manager_payroll.html",
        {
            "employee_data": employee_data,
            "hr_data": hr_data,
            "payroll_count": payroll_count,
            "today": today,
            "error_message": error_message,
        },
    )
