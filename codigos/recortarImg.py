<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:06ccef4b78e6b40f2b7a3f13639b3611d0fedc5b5c375614c75742b0b9f93a4f
size 831
=======
import cv2
import os

ruta = "./imagenes2"
# obtenemos una lista con los nombres de los archivos en la ruta especificada
archivos = os.listdir(ruta)
# Carga la imagen
for idx, archivo in enumerate(archivos):
    img = cv2.imread('./imagenes2/'+str(archivo))

    # Obtén las dimensiones de la imagen
    height, width = img.shape[:2]

    # Recorta la imagen
    cropped_img = img[0:height-500, 0:width]

    # Muestra la imagen original

    # Muestra la imagen recortada
    #rotated = cv2.rotate(cropped_img, cv2.ROTATE_180)

    #cv2.imshow('Imagen girada', rotated)
    #cv2.imshow('Imagen recortada', cropped_img)
    cv2.imwrite("./imagenes2new/imagen"+str(idx)+".jpg", cropped_img)
    #Espera hasta que se presione una tecla y cierra las ventanas
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
