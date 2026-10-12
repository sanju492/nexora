
from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    # Main Reports Dashboard
    path(
        "",
        views.reports_dashboard,
        name="reports_dashboard",
    ),

    # Send a new report
    path(
        "send/",
        views.send_report,
        name="send_report",
    ),

    # View received reports
    path(
        "inbox/",
        views.inbox_reports,
        name="inbox_reports",
    ),

    # View sent reports
    path(
        "sent/",
        views.sent_reports,
        name="sent_reports",
    ),

    # View an individual report
    path(
        "detail/<int:report_id>/",
        views.report_detail,
        name="report_detail",
    ),
]
