from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Attendance
from employees.models import EmployeeProfile


@login_required
def employee_attendance(request):

    employee = EmployeeProfile.objects.filter(
        user=request.user
    ).first()

    attendance_records = []

    if employee:
        attendance_records = Attendance.objects.filter(
            employee=employee
        ).order_by('-date', '-check_in')

    context = {
        'employee': employee,
        'attendance_records': attendance_records,
    }

    return render(
        request,
        'attendance/employee_attendance.html',
        context
    )


@login_required
def office_check_in(request):

    if request.method == 'POST':

        employee = EmployeeProfile.objects.filter(
            user=request.user
        ).first()

        if employee:

            today = timezone.localdate()
            current_time = timezone.localtime().time()

            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                work_mode='office',
                defaults={
                    'status': 'present',
                    'check_in': current_time,
                }
            )

            if not created and attendance.check_in is None:
                attendance.status = 'present'
                attendance.check_in = current_time
                attendance.save()

    return redirect('employee_attendance')


@login_required
def office_check_out(request):

    if request.method == 'POST':

        employee = EmployeeProfile.objects.filter(
            user=request.user
        ).first()

        if employee:

            today = timezone.localdate()

            attendance = Attendance.objects.filter(
                employee=employee,
                date=today,
                work_mode='office'
            ).first()

            if attendance and attendance.check_out is None:
                attendance.check_out = timezone.localtime().time()
                attendance.save()

    return redirect('employee_attendance')


@login_required
def wfh_check_in(request):

    if request.method == 'POST':

        employee = EmployeeProfile.objects.filter(
            user=request.user
        ).first()

        if employee:

            today = timezone.localdate()
            current_time = timezone.localtime().time()

            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                work_mode='wfh',
                defaults={
                    'status': 'present',
                    'check_in': current_time,
                }
            )

            if not created and attendance.check_in is None:
                attendance.status = 'present'
                attendance.check_in = current_time
                attendance.save()

    return redirect('employee_attendance')


@login_required
def wfh_check_out(request):

    if request.method == 'POST':

        employee = EmployeeProfile.objects.filter(
            user=request.user
        ).first()

        if employee:

            today = timezone.localdate()

            attendance = Attendance.objects.filter(
                employee=employee,
                date=today,
                work_mode='wfh'
            ).first()

            if attendance and attendance.check_out is None:
                attendance.check_out = timezone.localtime().time()
                attendance.save()

    return redirect('employee_attendance')


@login_required
def hr_attendance(request):

    employee = EmployeeProfile.objects.filter(
        user=request.user
    ).first()

    attendance_records = []

    if employee:
        attendance_records = Attendance.objects.filter(
            employee=employee
        ).order_by('-date', '-check_in')

    context = {
        'employee': employee,
        'attendance_records': attendance_records,
    }

    return render(
        request,
        'attendance/hr_attendance.html',
        context
    )


@login_required
def hr_office_check_in(request):

    if request.method == 'POST':

        employee = EmployeeProfile.objects.filter(
            user=request.user
        ).first()

        if employee:

            today = timezone.localdate()
            current_time = timezone.localtime().time()

            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                work_mode='office',
                defaults={
                    'status': 'present',
                    'check_in': current_time,
                }
            )

            if not created and attendance.check_in is None:
                attendance.status = 'present'
                attendance.check_in = current_time
                attendance.save()

    return redirect('hr_attendance')


@login_required
def hr_office_check_out(request):

    if request.method == 'POST':

        employee = EmployeeProfile.objects.filter(
            user=request.user
        ).first()

        if employee:

            today = timezone.localdate()

            attendance = Attendance.objects.filter(
                employee=employee,
                date=today,
                work_mode='office'
            ).first()

            if attendance and attendance.check_out is None:
                attendance.check_out = timezone.localtime().time()
                attendance.save()

    return redirect('hr_attendance')


@login_required
def hr_wfh_check_in(request):

    if request.method == 'POST':

        employee = EmployeeProfile.objects.filter(
            user=request.user
        ).first()

        if employee:

            today = timezone.localdate()
            current_time = timezone.localtime().time()

            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                work_mode='wfh',
                defaults={
                    'status': 'present',
                    'check_in': current_time,
                }
            )

            if not created and attendance.check_in is None:
                attendance.status = 'present'
                attendance.check_in = current_time
                attendance.save()

    return redirect('hr_attendance')


@login_required
def hr_wfh_check_out(request):

    if request.method == 'POST':

        employee = EmployeeProfile.objects.filter(
            user=request.user
        ).first()

        if employee:

            today = timezone.localdate()

            attendance = Attendance.objects.filter(
                employee=employee,
                date=today,
                work_mode='wfh'
            ).first()

            if attendance and attendance.check_out is None:
                attendance.check_out = timezone.localtime().time()
                attendance.save()

    return redirect('hr_attendance')