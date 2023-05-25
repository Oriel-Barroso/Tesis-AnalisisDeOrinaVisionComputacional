<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:eb79728c33354dfbfb79d07bd9991e28ed9a7845dd0c2fa2bdbbf68831e6dd7a
size 388
=======
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
>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
