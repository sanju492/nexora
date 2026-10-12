from django.db import models
from django.conf import settings


class Document(models.Model):
    DOCUMENT_TYPES = [
        ("resume", "Resume"),
        ("aadhaar", "Aadhaar Card"),
        ("pan", "PAN Card"),
        ("education", "Education Certificate"),
        ("experience", "Experience Letter"),
        ("salary_slip", "Salary Slip"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_documents",
    )

    title = models.CharField(max_length=150)
    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES,
        default="other",
    )
    file = models.FileField(upload_to="employee_documents/")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    remarks = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.title}"