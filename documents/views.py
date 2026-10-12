from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse

from .models import Document
from .forms import DocumentUploadForm


@login_required
def employee_documents(request):
    if getattr(request.user, "role", "") != "employee":
        messages.error(request, "Employee access only.")
        return redirect("home")

    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.employee = request.user
            document.status = "pending"
            document.save()

            messages.success(request, "Document uploaded successfully.")
            return redirect("documents:employee_documents")
    else:
        form = DocumentUploadForm()

    documents = Document.objects.filter(
        employee=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "documents/employee_documents.html",
        {"form": form, "documents": documents},
    )


@login_required
def download_employee_document(request, document_id):
    if getattr(request.user, "role", "") != "employee":
        messages.error(request, "Employee access only.")
        return redirect("home")

    document = get_object_or_404(
        Document,
        id=document_id,
        employee=request.user,
    )

    return FileResponse(
        document.file.open("rb"),
        as_attachment=True,
        filename=document.file.name.split("/")[-1],
    )
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Document


@login_required
def hr_documents(request):
    if getattr(request.user, "role", "") != "hr":
        messages.error(request, "HR access only.")
        return redirect("home")

    documents = Document.objects.select_related("employee").order_by(
        "-uploaded_at"
    )

    return render(
        request,
        "documents/hr_documents.html",
        {"documents": documents},
    )


@login_required
@require_POST
def review_document(request, document_id):
    if getattr(request.user, "role", "") != "hr":
        messages.error(request, "HR access only.")
        return redirect("home")

    document = get_object_or_404(Document, id=document_id)
    action = request.POST.get("action")
    remarks = request.POST.get("remarks", "").strip()

    if action == "approve":
        document.status = "approved"
        document.remarks = remarks
        document.save(update_fields=["status", "remarks"])
        messages.success(request, "Document approved successfully.")

    elif action == "reject":
        if not remarks:
            messages.error(request, "Please enter a reason before rejecting.")
            return redirect("documents:hr_documents")

        document.status = "rejected"
        document.remarks = remarks
        document.save(update_fields=["status", "remarks"])
        messages.success(request, "Document rejected.")

    else:
        messages.error(request, "Invalid action.")

    return redirect("documents:hr_documents")


@login_required
def hr_download_document(request, document_id):
    if getattr(request.user, "role", "") != "hr":
        messages.error(request, "HR access only.")
        return redirect("home")

    document = get_object_or_404(Document, id=document_id)

    from django.http import FileResponse

    return FileResponse(
        document.file.open("rb"),
        as_attachment=True,
        filename=document.file.name.split("/")[-1],
    )