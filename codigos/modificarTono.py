from PIL import Image
import random
# Carga la imagen
imagen = Image.open("./imagen1.jpeg")

# Convierte la imagen a modo de color HSV
imagen_hsv = imagen.convert("HSV")

# Obtén los componentes de color de la imagen
hue, saturation, value = imagen_hsv.split()

for col in range(0, 200):
    val = random.randint(1,6)
# Modifica el tono de la imagen
    hue = hue.point(lambda i: (i + col*val) % 256)

# Combina los componentes de color para formar la imagen resultante
    imagen_modificada = Image.merge("HSV", (hue, saturation, value)).convert("RGB")

# Guarda la imagen modificada
    imagen_modificada.save(f"imagen_modificada{col}.jpg")