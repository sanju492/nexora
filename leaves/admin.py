from django.contrib import admin
from .models import Leave


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):

    list_display = (
        'employee',
        'leave_type',
        'start_date',
        'end_date',
        'status',
        'applied_on',
    )

    list_filter = (
        'leave_type',
        'status',
        'start_date',
    )

    search_fields = (
        'employee__employee_id',
        'employee__user__username',
        'employee__user__first_name',
        'employee__user__last_name',
    )

    ordering = ('-applied_on',)