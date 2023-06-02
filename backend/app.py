import sys
import os
import ast
# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Obtener la ruta absoluta de la carpeta CarpetaB
yolo_dir = os.path.join(current_dir, '..', 'yolo')
carpeta_raiz_dir = os.path.dirname(current_dir)

# Añadir la ruta de yolo al path de búsqueda de módulos
sys.path.append(yolo_dir)
sys.path.append(carpeta_raiz_dir)


import detect_and_crop
import backend.diferenciaColor as diferenciaColor
from pdfConverter import PdfConverter
import datetime


def process_image(data):
    hora_actual = datetime.datetime.now()
    valuesDict = data['image']
    nombreCarpeta = 'imagenes'+ str(hora_actual.year) + str(hora_actual.month) \
            + str(hora_actual.day) + str(hora_actual.hour) + \
            str(hora_actual.minute) + str(hora_actual.second) + str(hora_actual.microsecond)
    source = createDirExist(nombreCarpeta)
    for nombreImagen, datosImagen in valuesDict.items():
        with open(source + nombreImagen, 'wb') as archivo:
            archivo.write(datosImagen)
    detc = detect_and_crop.DetectCrop(weights=yolo_dir+'/best.pt', source=source, image=current_dir+'/crop/')
    detc.detect()
    resultDifference = {}
    for nombreImagen in valuesDict.keys():
        resultDifference[nombreImagen] = checkDifferenceColors(nombreImagen[:nombreImagen.index('.')])
    resultsNew = checkResults(resultDifference)
    resultsNewDifference = []
    for nombreImagen in valuesDict.keys():
        if nombreImagen not in resultsNew.keys():
            resultsNewDifference.append(nombreImagen)
    if resultsNewDifference == []:
        pdf = PdfConverter(resultDifference)
        nombrePDF = pdf.createPDF()
        return {'pdf-name': nombrePDF, 'status': 'ok'}
    print(resultsNewDifference)
    return {'status': 'error', 'images': str(resultsNewDifference)}
    

def checkDifferenceColors(path):
    dif = diferenciaColor.DiferenciaColores(path)
    val = dif.main()
    return val

def createDirExist(image):
    if not os.path.exists(current_dir+"/imgEnt/"+image):
        os.makedirs(current_dir+"/imgEnt/"+image)
    return current_dir+"/imgEnt/"+image+'/'

def checkResults(results):
    resultsNew = {}
    for k,v in results.items():
        if len(v) == 10:
            resultsNew[k] = v
    return resultsNew

if __name__ == "__main__":
    app.run(debug=False)
