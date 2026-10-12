from django.db import models


class Attendance(models.Model):

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('leave', 'Leave'),
    )

    WORK_MODE_CHOICES = (
        ('office', 'Office'),
        ('wfh', 'Work From Home'),
    )

    employee = models.ForeignKey(
        'employees.EmployeeProfile',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    date = models.DateField()

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='present'
    )

    work_mode = models.CharField(
        max_length=10,
        choices=WORK_MODE_CHOICES,
        default='office'
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'date', 'work_mode'],
                name='unique_employee_date_work_mode'
            )
        ]

        ordering = ['-date', '-check_in']

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.date} - "
            f"{self.work_mode}"
        )