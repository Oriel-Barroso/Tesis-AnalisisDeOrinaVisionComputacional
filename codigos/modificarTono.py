# <<<<<<< HEAD
# version https://git-lfs.github.com/spec/v1
# oid sha256:c44c78b032b4afdd559c4a8422ae189a39d1de8bc11542ba8f7e945d368b0ec4
# size 663
# =======
from PIL import Image
import random
# Carga la imagen
imagen = Image.open("./newImages/imagenes1.jpeg")

# Convierte la imagen a modo de color HSV
imagen_hsv = imagen.convert("HSV")

# Obtén los componentes de color de la imagen
hue, saturation, value = imagen_hsv.split()

for col in range(0, 30):
    val = random.randint(1,6)
# Modifica el tono de la imagen
    hue = hue.point(lambda i: (i + col*val) % 256)

# Combina los componentes de color para formar la imagen resultante
    imagen_modificada = Image.merge("HSV", (hue, saturation, value)).convert("RGB")

# Guarda la imagen modificada
    imagen_modificada.save(f"imagen_modificada{col}.jpg")
#>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
