from django.contrib import admin
from .models import EmployeeProfile


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'user',
        'designation',
        'gender',
        'joining_date',
        'salary',
    )

    list_filter = (
        'gender',
        'designation',
        'joining_date',
    )

    search_fields = (
        'employee_id',
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
    )

    ordering = ('employee_id',)