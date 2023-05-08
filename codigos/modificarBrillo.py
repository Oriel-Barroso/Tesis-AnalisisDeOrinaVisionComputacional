from PIL import Image, ImageStat

# Abrir la imagen
imagen = Image.open('./TiraSinReaccionar2/l1.jpg')

# Calcular las estadísticas de la imagen
estadisticas = ImageStat.Stat(imagen)

# Obtener el brillo promedio actual de la imagen
brillo_promedio_actual = estadisticas.mean[0]

# Calcular la diferencia entre el brillo promedio actual y el deseado
diferencia = 30 - brillo_promedio_actual

# Crear una función de transformación lineal que ajuste el brillo
def ajustar_brillo(valor):
    return int(valor + diferencia)

# Aplicar la transformación de brillo a la imagen
imagen_ajustada = imagen.point(ajustar_brillo)

# Guardar la imagen ajustada en un archivo
imagen_ajustada.save('imagen_ajustada.jpg')