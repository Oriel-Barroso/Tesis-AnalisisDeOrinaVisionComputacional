# <<<<<<< HEAD
# version https://git-lfs.github.com/spec/v1
# oid sha256:9b74ccba99e7f3bdeef761a31c9f91e952983f43c013cb360248029f3742a6d9
# size 1816
# =======
from PIL import Image

# Abre la primera imagen
img1 = Image.open('./crop/0.jpg')

# Convierte la primera imagen a modo RGB
img1 = img1.convert('RGB')

# Obtiene el ancho y alto de la primera imagen
width1, height1 = img1.size

# Crea una matriz vacía para almacenar los valores de color RGB de la primera imagen
pixels1 = [[0 for x in range(width1)] for y in range(height1)]

# Itera sobre cada píxel de la primera imagen y almacena su valor de color RGB en la matriz
for y in range(height1):
    for x in range(width1):
        pixels1[y][x] = img1.getpixel((x, y))

# Abre la segunda imagen
img2 = Image.open('./colores/0/ery1.jpeg') #dg7 para 6

# Convierte la segunda imagen a modo RGB
img2 = img2.convert('RGB')

# Obtiene el ancho y alto de la segunda imagen
width2, height2 = img2.size

# Crea una matriz vacía para almacenar los valores de color RGB de la segunda imagen
pixels2 = [[0 for x in range(width2)] for y in range(height2)]

# Itera sobre cada píxel de la segunda imagen y almacena su valor de color RGB en la matriz
for y in range(height2):
    for x in range(width2):
        pixels2[y][x] = img2.getpixel((x, y))

# Compara ambas matrices y calcula su similitud
similarity = 0
for y in range(min(height1, height2)):
    for x in range(min(width1, width2)):
        r1, g1, b1 = pixels1[y][x]
        r2, g2, b2 = pixels2[y][x]
        similarity += abs(r1-r2) + abs(g1-g2) + abs(b1-b2)
        
# Calcula el promedio de la similitud
avg_similarity = similarity / (min(height1, height2) * min(width1, width2) * 3)
print(avg_similarity)
# Imprime el resultado
if avg_similarity < 50:
    print('Las imágenes son muy parecidas en términos de color.')
else:
    print('Las imágenes son diferentes en términos de color.')
#>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
