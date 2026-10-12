from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "document_type", "file"]

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")

        if uploaded_file:
            allowed_extensions = (
                ".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"
            )

            if not uploaded_file.name.lower().endswith(allowed_extensions):
                raise forms.ValidationError("Unsupported file format.")

            if uploaded_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Maximum file size is 5 MB.")

        return uploaded_file