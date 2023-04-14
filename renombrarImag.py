import os


# ruta del directorio donde se encuentran las imágenes
ruta = r"C:\Users\Oriel\Documents\testIA\imagenes"

# obtenemos una lista con los nombres de los archivos en la ruta especificada
archivos = os.listdir(ruta)

# iteramos sobre cada archivo en la lista
for idx, archivo in enumerate(archivos):
    # comprobamos si el archivo es una imagen jpeg
    if archivo.endswith(".jpg") or archivo.endswith(".jpeg"):
        os.rename(os.path.join(ruta, archivo), os.path.join(ruta, "imagen" + str(idx) + ".jpg"))
