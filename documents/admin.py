from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = (
        'employee',
        'document_type',
        'title',
        'uploaded_at',
    )

    list_filter = (
        'document_type',
        'uploaded_at',
    )

    search_fields = (
        'title',
        'employee__employee_id',
        'employee__user__username',
        'employee__user__first_name',
        'employee__user__last_name',
    )

    ordering = ('-uploaded_at',)