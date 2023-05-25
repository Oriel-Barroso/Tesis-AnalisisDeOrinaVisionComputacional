# <<<<<<< HEAD
# version https://git-lfs.github.com/spec/v1
# oid sha256:99319edc4b317127352d078c22782a1c2750891f8eb39e84fcc0762a357dd027
# size 548
# =======
import os

# ruta del directorio donde se encuentran las imágenes
ruta = "/mnt/c/Users/Admin/Documents/Universidad/testIA/imagenes"

# obtenemos una lista con los nombres de los archivos en la ruta especificada
archivos = os.listdir(ruta)

# iteramos sobre cada archivo en la lista
for idx, archivo in enumerate(archivos):
    # comprobamos si el archivo es una imagen jpeg
    if archivo.endswith(".jpg") or archivo.endswith(".jpeg"):
        os.rename(os.path.join(ruta, archivo), os.path.join(ruta, "imagen_" + str(idx) + ".jpg"))
# >>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
