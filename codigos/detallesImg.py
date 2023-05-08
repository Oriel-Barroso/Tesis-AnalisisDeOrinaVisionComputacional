import cv2
import os

ruta = "./imagenes_recortadas"
# obtenemos una lista con los nombres de los archivos en la ruta especificada
archivos = os.listdir(ruta)
# Carga la imagen
c = 0
for idx, archivo in enumerate(archivos):
    img = cv2.imread('./imagenes_recortadas/'+str(archivo))
    height, weight = img.shape[:2]
    if height > 30 or weight > 30:
        c+=1
print(c)