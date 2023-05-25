from PIL import Image
import numpy as np

imagen = Image.open("img13.jpeg")  # Reemplaza "ruta_de_tu_imagen.jpg" con la ruta de tu imagen

# Aumento de la saturación
factor_saturacion = 1.05  # Puedes ajustar este valor según tus preferencias, un valor mayor a 1 aumentará la saturación

imagen_array = np.array(imagen)  # Convierte la imagen en un arreglo NumPy para manipular los valores de color

# Aumento de los valores de color en cada píxel
imagen_array_aumentada = np.clip(imagen_array * factor_saturacion, 0, 255).astype(np.uint8)

imagen_aumentada = Image.fromarray(imagen_array_aumentada)  # Convierte el arreglo NumPy de vuelta a imagen

imagen_aumentada.save("imgAum.jpg")