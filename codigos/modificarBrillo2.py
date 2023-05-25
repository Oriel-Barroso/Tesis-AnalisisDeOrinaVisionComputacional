from PIL import Image, ImageEnhance, ImageStat

img = Image.open("pruebas/img3.jpeg").convert("RGB")

img_enhancer = ImageEnhance.Contrast(img)


estadisticas = ImageStat.Stat(img)
brillo_promedio = estadisticas.mean[0]
factor = 1
# Obtener el brillo promedio de la imagen
brightness = 0
while brightness < 180:
    enhanced_output = img_enhancer.enhance(factor)
    est = ImageStat.Stat(enhanced_output)
    brightness = est.mean[0]
    factor+=0.2

enhanced_output.save("original-image.jpeg")