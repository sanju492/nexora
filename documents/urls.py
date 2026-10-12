from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    # Employee Documents
    path(
        "employee/",
        views.employee_documents,
        name="employee_documents",
    ),
    path(
        "download/<int:document_id>/",
        views.download_employee_document,
        name="download_employee_document",
    ),

    # HR Documents
    path(
        "hr/",
        views.hr_documents,
        name="hr_documents",
    ),
    path(
        "hr/review/<int:document_id>/",
        views.review_document,
        name="review_document",
    ),
    path(
        "hr/download/<int:document_id>/",
        views.hr_download_document,
        name="hr_download_document",
    ),
]