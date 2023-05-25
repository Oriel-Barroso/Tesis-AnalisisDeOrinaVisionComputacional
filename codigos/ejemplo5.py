<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:7e3518cefbdf7c1c4d9b86481cc6344c7cd590a2d08931748c7d268ec9697a30
size 1321
=======
import cv2
import numpy as np

# Leer la imagen del test de orina
image = cv2.imread('imagen11.jpg')

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar un filtro gaussiano para reducir el ruido
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Aplicar la umbralización para separar las almohadillas del fondo
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# Aplicar la operación de apertura morfológica para eliminar pequeñas imperfecciones
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# Buscar los contornos en la imagen
cnts, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterar sobre los contornos encontrados
for cnt in cnts:
    # Aproximar el contorno a una forma poligonal
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    
    # Si la forma poligonal tiene cuatro lados, dibujar un rectángulo alrededor del contorno
    #if len(approx) == 4:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Mostrar la imagen con los rectángulos dibujados
cv2.imshow('Almohadillas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
