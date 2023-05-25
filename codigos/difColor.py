# <<<<<<< HEAD
# version https://git-lfs.github.com/spec/v1
# oid sha256:c0a8965b4b3505348233c002839c152dbb6fd6f94725f3caed57bc38874980c9
# size 2452
# =======
import cv2
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor
import os

class DiferenciaColores():
    def __init__(self, ruta):
        self.ruta = str(ruta)
        self.imagenesA = {}
        self.imagenesB = {}
        self.imagenesLabA = []
        self.imagenesLabB = []
        self.block_size_x = []
        self.block_size_y = [] 
        self.color_meansA = {} 
        self.color_meansB = {}

    # Función para calcular la diferencia Delta E 2000 entre dos valores de color
    def delta_e_2000(color1, color2):
        lab1 = LabColor(color1[0], color1[1], color1[2])
        lab2 = LabColor(color2[0], color2[1], color2[2])
        return delta_e_cie2000(lab1, lab2)

    def leerImgs(self, dicc):
        archivos = os.listdir(self.ruta)
        for archivo in archivos:
            if archivo.endswith(".jpg") or archivo.endswith(".jpeg"):  
                    dicc[archivo] = cv2.imread(str(archivo))
        return dicc

    def colorAlab(self, dictImagenes, dictImagenesLab):
        for clave, imagen in dictImagenes.items():
            dictImagenesLab[clave] = cv2.cvtColor(imagen, cv2.COLOR_BGR2LAB)
        return dictImagenesLab
    

    # Convertir las imágenes al espacio de color LAB
    # lab_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
    # lab_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)


    def calcularTamañoBloque(self, dictImagenLabA, dictImagenLabB):
        num_blocks_x = 4
        num_blocks_y = 4
        # Calcular el tamaño de cada bloque
        color_mean1 = {}
        for claveA, lab_img1 in dictImagenLabA.items():
            block_size_x = int(lab_img1.shape[1] / num_blocks_x)
            block_size_y = int(lab_img1.shape[0] / num_blocks_y)

            # Calcular el valor de color medio para cada bloque en ambas imágenes
            for i in range(num_blocks_y):
                for j in range(num_blocks_x):
                    # Calcular el índice del bloque actual
                    block_start_x = j * block_size_x
                    block_start_y = i * block_size_y
                    block_end_x = block_start_x + block_size_x
                    block_end_y = block_start_y + block_size_y
                    for claveB, lab_img2 in dictImagenLabB.items():
                        block_mean1 = cv2.mean(lab_img1[block_start_y:block_end_y, block_start_x:block_end_x])
                        # Calcular el valor de color medio para el bloque actual en la segunda imagen
                        block_mean2 = cv2.mean(lab_img2[block_start_y:block_end_y, block_start_x:block_end_x])
                        # Asegurarse de que la longitud de las listas sea la misma antes de agregar los valores medios de color
                        if len(self.color_meansA) == len(self.color_meansB):
                            self.color_meansA[claveA] = [(block_mean1[0], block_mean1[1], block_mean1[2])]
                            self.color_meansB[claveB] = (block_mean2[0], block_mean2[1], block_mean2[2])

                            self.color_meansA.append((block_mean1[0], block_mean1[1], block_mean1[2]))
                            self.color_meansB.append((block_mean2[0], block_mean2[1], block_mean2[2]))

    def diferencia(self):
        # Calcular la diferencia Delta E 2000 entre los valores de color medios de cada bloque en ambas imágenes
        differences = []
        for i in range(len(self.color_meansA)):
            differences.append(self.delta_e_2000(self.color_meansA[i], self.color_meansB[i]))
        # Calcular el promedio de todas
        average_difference = sum(differences) / len(differences)
        print("La diferencia media entre los colores de las dos imágenes es:", average_difference)

    def run(self):
        rutaImgCrop = './crop/'
        #imgCrop = {0: '', ..., 9: ''}

    # >>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
