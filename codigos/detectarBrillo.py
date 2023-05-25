# <<<<<<< HEAD
# version https://git-lfs.github.com/spec/v1
# oid sha256:84c47eb4131028a325928b547db307fa91a047aca7fd66d1484d81bd5a9d41f4
# size 341
# =======

from PIL import Image, ImageStat

# Abrir la imagen
imagen = Image.open('./img13.jpeg')

# Calcular las estadísticas de la imagen
estadisticas = ImageStat.Stat(imagen)

# Obtener el brillo promedio de la imagen
brillo_promedio = estadisticas.mean[0]

print(f'El brillo promedio de la imagen es {brillo_promedio}.')

#>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
