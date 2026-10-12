
from django.db import models


class Payroll(models.Model):

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    )

    employee = models.ForeignKey(
        'employees.EmployeeProfile',
        on_delete=models.CASCADE,
        related_name='payroll_records'
    )

    month = models.DateField(
        verbose_name='Payroll Month'
    )

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    allowances = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    paid_on = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        # Set paid date when status changes to Paid.
        if self.payment_status == 'paid' and self.paid_on is None:
            from django.utils import timezone
            self.paid_on = timezone.localdate()

        # Clear paid date if status returns to Pending.
        elif self.payment_status == 'pending':
            self.paid_on = None

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.month.strftime('%B %Y')}"
        )
