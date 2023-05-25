<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:fd901ac781b801fb82d2900f03b9187b5d9d9a4c2e070f2772602c5d190a7a0b
size 969
=======
import tensorflow as tf
import os
from PIL import Image
import numpy as np

modelo = tf.keras.models.load_model(r"C:\Users\Admin\Documents\testIA\modelo")

"""Traer imagen"""
carpeta = r'C:\Users\Admin\Documents\Images\Dataset\Test\sample2'
archivos = os.listdir(carpeta)
imagenes = [archivo for archivo in archivos if archivo.endswith('.jpg') or archivo.endswith('.jpeg') or archivo.endswith('.png')]
resultados = []
for imagen in imagenes:
    ruta_imagen = os.path.join(carpeta, imagen)
    with Image.open(ruta_imagen) as img:
        img1= np.array(img)/255.
        img2=tf.reshape(img1, shape=(1,150,150,3))
        img3 = tf.expand_dims(img2, axis=0)
        resultado = modelo.predict(img3)
        resultados.append(resultado)

# Imprime los resultados
for i, resultado in enumerate(resultados):
    imagen = imagenes[i]
    print(f'La imagen {imagen} fue clasificada como {resultado}')
print('end')
"""Para redondear tf.round()"""
>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
