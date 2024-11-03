# Necessarry Libraries
from django import forms

# A form to upload a PDF file
class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField()

# A form to upload an image
class ImageUploadForm(forms.Form):
    img_file = forms.ImageField()