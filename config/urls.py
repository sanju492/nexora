
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as account_views

urlpatterns = [
    # Home
    path("", account_views.home, name="home"),

    # Django Admin
    path("admin/", admin.site.urls),

    # Accounts and dashboards
    path("accounts/", include("accounts.urls")),

    # Employee management
    path("employees/", include("employees.urls")),

    # Attendance management
    path("attendance/", include("attendance.urls")),

    # Leave management
    path("leaves/", include("leaves.urls")),

    # Reports
    path("reports/", include("reports.urls")),

    # Payroll
    path("payroll/", include("payroll.urls")),

    # Documents
    path("documents/", include("documents.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
