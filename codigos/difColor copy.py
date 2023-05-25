# <<<<<<< HEAD
# version https://git-lfs.github.com/spec/v1
# oid sha256:c0a8965b4b3505348233c002839c152dbb6fd6f94725f3caed57bc38874980c9
# size 2452
# =======
import cv2
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor

# Función para calcular la diferencia Delta E 2000 entre dos valores de color
def delta_e_2000(color1, color2):
    lab1 = LabColor(color1[0], color1[1], color1[2])
    lab2 = LabColor(color2[0], color2[1], color2[2])
    return delta_e_cie2000(lab1, lab2)

# Cargar las imágenes
img1 = cv2.imread('./crop/0.jpg')
img2 = cv2.imread('./colores/0/ery4A.jpeg')

# Convertir las imágenes al espacio de color LAB
lab_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
lab_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)

# Definir la cantidad de bloques en cada dirección
num_blocks_x = 4
num_blocks_y = 4

# Calcular el tamaño de cada bloque
block_size_x = int(lab_img1.shape[1] / num_blocks_x)
block_size_y = int(lab_img1.shape[0] / num_blocks_y)

# Calcular el valor de color medio para cada bloque en ambas imágenes
color_means1 = []
color_means2 = []

for i in range(num_blocks_y):
    for j in range(num_blocks_x):
        # Calcular el índice del bloque actual
        block_start_x = j * block_size_x
        block_start_y = i * block_size_y
        block_end_x = block_start_x + block_size_x
        block_end_y = block_start_y + block_size_y
        
        # Calcular el valor de color medio para el bloque actual en la primera imagen
        block_mean1 = cv2.mean(lab_img1[block_start_y:block_end_y, block_start_x:block_end_x])
        
        # Calcular el valor de color medio para el bloque actual en la segunda imagen
        block_mean2 = cv2.mean(lab_img2[block_start_y:block_end_y, block_start_x:block_end_x])
        
        # Asegurarse de que la longitud de las listas sea la misma antes de agregar los valores medios de color
        if len(color_means1) == len(color_means2):
            color_means1.append((block_mean1[0], block_mean1[1], block_mean1[2]))
            color_means2.append((block_mean2[0], block_mean2[1], block_mean2[2]))

# Calcular la diferencia Delta E 2000 entre los valores de color medios de cada bloque en ambas imágenes
differences = []
for i in range(len(color_means1)):
    differences.append(delta_e_2000(color_means1[i], color_means2[i]))


# Calcular el promedio de todas
average_difference = sum(differences) / len(differences)

print("La diferencia media entre los colores de las dos imágenes es:", average_difference)
# >>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
