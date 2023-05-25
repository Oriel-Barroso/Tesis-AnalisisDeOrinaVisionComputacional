<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:3d8fa3395c53061a241c8e5c9f37d4a4033176b48a65740837ce903c313c6387
size 1018
=======
import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread("/mnt/c/Users/Admin/Documents/imgEnt/imagen1.jpg")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definir un rango de valores de color amarillo en HSV
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([40, 255, 255])

# Crear una máscara utilizando los valores de color amarillo definidos
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# Encontrar los contornos en la imagen
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterar sobre los contornos y recortar las regiones rectangulares
for i, contour in enumerate(contours):
    # Obtener las coordenadas del rectángulo delimitador
    x,y,w,h = cv2.boundingRect(contour)
    # Recortar la región rectangular y guardarla
    if w >= 80 and h >= 49:
        # Recortar la región rectangular y guardarla
        cropped_image = image[y:y+h, x:x+w]
        cv2.imwrite(f"cuadrado_{i}.jpg", cropped_image)
>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
