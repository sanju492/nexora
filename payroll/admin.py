
from django.contrib import admin
from .models import Payroll


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'month',
        'basic_salary',
        'allowances',
        'deductions',
        'net_salary',
        'payment_status',
        'paid_on',
    )

    list_filter = (
        'payment_status',
        'month',
    )

    search_fields = (
        'employee__employee_id',
        'employee__user__username',
        'employee__user__first_name',
        'employee__user__last_name',
    )

    ordering = ('-month',)
