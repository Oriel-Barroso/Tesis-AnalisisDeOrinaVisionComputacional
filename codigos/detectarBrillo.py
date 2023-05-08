from PIL import Image, ImageStat

# Abrir la imagen
imagen = Image.open('./TiraSinReaccionar2/l1.jpg')

# Calcular las estadísticas de la imagen
estadisticas = ImageStat.Stat(imagen)

# Obtener el brillo promedio de la imagen
brillo_promedio = estadisticas.mean[0]

print(f'El brillo promedio de la imagen es {brillo_promedio}.')