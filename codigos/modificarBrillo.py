# <<<<<<< HEAD
# version https://git-lfs.github.com/spec/v1
# oid sha256:47437105aa5f3f9c55648dcc3c39e3dcc8c25206ab735672ce760b407c2e0cef
# size 731
# =======
from PIL import Image, ImageStat

# Abrir la imagen
imagen = Image.open('./tiraReaccionada/1.jpeg')
imagen2 = Image.open('./tiraReaccionada/imagen1.jpeg')
# Calcular las estadísticas de la imagen
estadisticas = ImageStat.Stat(imagen)
estadisticas2 = ImageStat.Stat(imagen2)
# Obtener el brillo promedio actual de la imagen
brillo_promedio_actual = estadisticas.mean[0]
brillo_promedio_actual2 = estadisticas2.mean[0]

# Calcular la diferencia entre el brillo promedio actual y el deseado
diferencia = brillo_promedio_actual
# Crear una función de transformación lineal que ajuste el brillo
def ajustar_brillo(valor):
    return int(valor + diferencia)

# Aplicar la transformación de brillo a la imagen
imagen_ajustada = imagen2.point(ajustar_brillo)

# Guardar la imagen ajustada en un archivo
imagen_ajustada.save('imagen_ajustada.jpg')
#>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
