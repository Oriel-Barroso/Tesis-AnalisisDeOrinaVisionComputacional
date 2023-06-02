from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime



class PdfConverter():
    def __init__(self, resultados):
        self.resultados = resultados

    def createPDF(self):
        hora_actual = datetime.datetime.now()
        nombrePDF = 'resultados' + str(hora_actual.year) + str(hora_actual.month) \
            + str(hora_actual.day) + str(hora_actual.hour) + \
            str(hora_actual.minute) + str(hora_actual.second) \
            + str(hora_actual.microsecond) + '.pdf'
        pdf = canvas.Canvas(nombrePDF, pagesize=letter)

        # Establecer título en la primera página
        pdf.setTitle("TESTRINE")
        
        # Configurar formato del título
        pdf.setFont("Helvetica-Bold", 16)
        
        # Centrar el título en la página
        titulo = "TESTRINE"
        titulo_width = pdf.stringWidth(titulo, "Helvetica-Bold", 16)
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
        return nombrePDF

