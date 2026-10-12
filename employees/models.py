from django.conf import settings
from django.db import models


class EmployeeProfile(models.Model):

    # APPROVAL STATUS
    APPROVAL_STATUS_CHOICES = (
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    # GENDER
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    # USER
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )

    # APPROVAL STATUS
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default="pending",
    )

    approved_by = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    rejected_by = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    # DEPARTMENT
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )

    # EMPLOYEE ID
    employee_id = models.CharField(
        max_length=20,
        unique=True,
    )

    # DESIGNATION
    designation = models.CharField(
        max_length=100,
    )

    # GENDER
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
    )

    # DATE OF BIRTH
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    # ADDRESS
    address = models.TextField(
        blank=True,
    )

    # JOINING DATE
    joining_date = models.DateField()

    # SALARY
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # CREATED AT
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # STRING REPRESENTATION
    def __str__(self):
        return (
            f"{self.employee_id} - "
            f"{self.user.get_full_name() or self.user.username}"
        )