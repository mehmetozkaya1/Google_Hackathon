# Necessarry libraries
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import textwrap

# A function to create a PDF file contains the questions
def create_pdf(text_data, file_name):
    pdf_canvas = canvas.Canvas(file_name, pagesize=A4) # Create a canvas
    width, height = A4 # Adjust the width and the height

    # Font file path
    font_path = f"pages/static/fonts/font1.ttf"
    pdfmetrics.registerFont(TTFont('TurkishFont', font_path))
    pdf_canvas.setFont("TurkishFont", 12)

    # Background color
    pdf_canvas.setFillColorRGB(0.9, 0.9, 0.9)
    pdf_canvas.rect(0, 0, width, height, fill=True, stroke=False)

    # Page border
    pdf_canvas.setStrokeColorRGB(0, 0, 0)
    pdf_canvas.setLineWidth(1)
    pdf_canvas.rect(40, 40, width - 80, height - 80)

    # Title
    pdf_canvas.setFont('TurkishFont', 18)
    pdf_canvas.setFillColorRGB(0, 0, 0)  
    pdf_canvas.drawString(50, height - 70, "Sorular")

    # File location variables
    x = 50
    y = height - 100

    # Text font
    pdf_canvas.setFont('TurkishFont', 12)

    for line in text_data.split("\n"):
        if line.strip() == "":
            y -= 10
            continue

        wrapped_lines = textwrap.wrap(line, width=80)  

        for wrap_line in wrapped_lines:
            pdf_canvas.drawString(x, y, wrap_line)
            y -= 15

            if y < 50:
                pdf_canvas.showPage()

                pdf_canvas.setFillColorRGB(0.9, 0.9, 0.9)
                pdf_canvas.rect(0, 0, width, height, fill=True, stroke=False)
                pdf_canvas.setStrokeColorRGB(0, 0, 0)
                pdf_canvas.setLineWidth(1)
                pdf_canvas.rect(40, 40, width - 80, height - 80)
                
                pdf_canvas.setFont('TurkishFont', 18)
                pdf_canvas.setFillColorRGB(0, 0, 0)

                pdf_canvas.setFont('TurkishFont', 12)
                y = height - 100

    # Save the PDF file
    pdf_canvas.save()
