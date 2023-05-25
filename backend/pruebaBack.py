import sys
import os
# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Obtener la ruta absoluta de la carpeta CarpetaB
yolo_dir = os.path.join(current_dir, '..', 'yolo')
carpeta_raiz_dir = os.path.dirname(current_dir)

# Añadir la ruta de CarpetaB al path de búsqueda de módulos
sys.path.append(yolo_dir)
sys.path.append(carpeta_raiz_dir)

# Importar archivoB desde CarpetaB
import detect_and_crop
import diferenciaColor
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)


@app.route("/im_size", methods=["POST"])
def process_image():
    hora_actual = datetime.datetime.now()
    data = request.files['image']
    dataImg = request.files['name-image'].stream.read().decode()
    image = 'imagen'+str(hora_actual.hour) + \
    str(hora_actual.minute)+str(hora_actual.second)+'.jpeg'
    imageWithoutExtension = image[:image.index('.')]
    # source = createDirExist(imageWithoutExtension)
    # data.save(source+image)
    # detc = detect_and_crop.DetectCrop(weights='yolo/best.pt', source=source, image=imageWithoutExtension)
    # detc.detect()
    # val = checkDifferenceColors(imageWithoutExtension)
    val = "Imagen guardada: "+dataImg
    return jsonify({'lista': f'{val}', 'name-image': dataImg})

def checkDifferenceColors(path):
    dif = diferenciaColor.DiferenciaColores(path)
    val = dif.main()
    return val

def createDirExist(image):
    if not os.path.exists("backend/imgEnt/"+image):
        os.mkdir("backend/imgEnt/"+image)
    return "backend/imgEnt/"+image+'/'


if __name__ == "__main__":
    app.run(debug=True)
