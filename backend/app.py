import shutil
import sys
import os
import diferenciaColor as diferenciaColor
from pdfConverter import PdfConverter
import datetime
from excelConverter import CreateExcel

current_dir = os.path.dirname(os.path.abspath(__file__))
yolo_dir = os.path.join(current_dir, '..', 'yolo')
carpeta_raiz_dir = os.path.dirname(current_dir)
sys.path.append(yolo_dir)
sys.path.append(carpeta_raiz_dir)

import detect_and_crop


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
    resultExcel = {}
    resultError = []
    resultOK = []
    for nombreImagen in valuesDict.keys():
        valor = checkDifferenceColors(nombreImagen[:nombreImagen.index('.')])
        if len(valor) == 10:
            resultDifference[nombreImagen] = valor
            resultExcel[nombreImagen] = createDict(valor)
            resultOK.append(nombreImagen)
        else:
            resultError.append(nombreImagen)
    if len(resultDifference) != 0 and len(resultExcel) != 0:
        pdf = PdfConverter(resultDifference)
        pdf.createPDF()
        excel = CreateExcel(resultExcel)
        excel.createExl()
    deleteDirs(source)
    for nombreImagen in valuesDict.keys():
        print(nombreImagen)
        deleteDirs(current_dir+'/crop/'+nombreImagen[:nombreImagen.index('.')])
    return {'imagesOK': resultOK, 'imagesError': resultError}


def checkDifferenceColors(path):
    dif = diferenciaColor.DiferenciaColores(path)
    val = dif.main()
    return val


def createDirExist(image):
    if not os.path.exists(current_dir+"/imgEnt/"+image):
        os.makedirs(current_dir+"/imgEnt/"+image)
    return current_dir+"/imgEnt/"+image+'/'


def deleteDirs(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def createDict(lista):
    try:
        dic = {'Sangre': None, 'Bilirruina': None, 'Urobilinogeno': None, 
                'Cuerpos cetonicos': None, 'Glucosa': None, 'Proteina': None, 
                'Nitrito': None, 'Leucocitos': None, 'pH': None, 
                'Densidad relativa': None}
        i = 0
        for k in dic.keys():
            dic[k] = lista[i][lista[i].index(': ')+1:].replace(" ", "") # Toma el valor de la lista, busca el valor despues de los 2 puntos y borra el espacio
            i += 1
        return dic
    except Exception:
        raise IndexError
