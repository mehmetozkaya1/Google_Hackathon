# Necessarry libraries
from django.db import models

# A model to get a PDF documnet
class PDFDocument(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pdf_file.name