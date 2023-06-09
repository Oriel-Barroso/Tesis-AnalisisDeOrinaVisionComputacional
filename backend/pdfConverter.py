from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class PdfConverter():
    def __init__(self, resultados):
        self.resultados = resultados

    def createPDF(self):
        nombrePDF = 'resultados.pdf'
        pdf = canvas.Canvas(nombrePDF, pagesize=letter)
        pdf.setTitle("TESTRINE")
        pdf.setFont("Helvetica-Bold", 16)
        titulo = "TESTRINE"
        pdf.drawCentredString(pdf._pagesize[0] / 2, pdf._pagesize[1] - 50, titulo)
        pdf.setFont("Helvetica", 12)
        x = 50
        y = pdf._pagesize[1] - 70  # Ajustar la posición vertical para dejar espacio para el título
        for imagen, valores in self.resultados.items():
            # Verificar si hay suficiente espacio vertical en la página actual
            if y < 50:
                pdf.showPage()  # Pasar a una nueva página
                y = pdf._pagesize[1] - 70  # Reiniciar la posición vertical para la nueva página
            pdf.drawString(x, y, f'Resultados de {imagen}:')
            y -= 20
            for valor in valores:
                # Verificar si hay suficiente espacio vertical en la página actual
                if y < 50:
                    pdf.showPage()  # Pasar a una nueva página
                    y = pdf._pagesize[1] - 70  # Reiniciar la posición vertical para la nueva página
                pdf.drawString(x + 20, y, f'- {valor}')
                y -= 20
        pdf.save()
