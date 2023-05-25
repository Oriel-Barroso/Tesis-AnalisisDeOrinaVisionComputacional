from PIL import Image
import numpy as np

imagen_referencia = Image.open("./tiraReaccionada/1.jpeg")
brillo_referencia = np.mean(imagen_referencia)
contraste_referencia = np.std(imagen_referencia)

lista_rutas_imagenes = ["./tiraReaccionada/imagen1A.jpeg", "./tiraReaccionada/imagen1.jpeg", "./tiraReaccionada/imagen2.jpeg", "./tiraReaccionada/imagen3.jpeg"]

for ruta_imagen in lista_rutas_imagenes:
    imagen = Image.open(ruta_imagen)

    brillo_actual = np.mean(imagen)
    contraste_actual = np.std(imagen)

    # Ajuste de brillo
    diferencia_brillo = brillo_referencia - brillo_actual
    diferencia_brillo2 = diferencia_brillo + brillo_actual
    imagen_ajustada = np.array(imagen) + diferencia_brillo2

    # Ajuste de contraste
    diferencia_contraste = contraste_referencia / contraste_actual
    imagen_ajustada = np.array(imagen_ajustada * diferencia_contraste, dtype=np.uint8)

    imagen_ajustada_pil = Image.fromarray(imagen_ajustada)
    ruta_imagen_ajustada = "./imgModif/" + ruta_imagen.split("/")[-1]  # Ruta de destino para la imagen ajustada
    imagen_ajustada_pil.save(ruta_imagen_ajustada)