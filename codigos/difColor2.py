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
    def __init__(self):
        self.color_means = {} 

    def delta_e_2000(self, color1, color2):
        lab1 = LabColor(color1[0], color1[1], color1[2])
        lab2 = LabColor(color2[0], color2[1], color2[2])
        return delta_e_cie2000(lab1, lab2)


    def getRutaColores(self, carpetas):
        lista = []
        for i in range(0, len(carpetas)):
            lista.append('./colores/'+carpetas[i])
        return lista
    

    def leerImgs(self, ruta):
        archivos = os.listdir(ruta)
        dicc = {}
        for archivo in archivos:
            if archivo.endswith(".jpg") or archivo.endswith(".jpeg"):  
                    dicc[archivo] = cv2.imread(ruta+'/'+archivo)
        return dicc


    def leerColores(self, ruta):
        archivos = os.listdir(ruta)
        dic = {}
        for archivo in archivos:
            if archivo.endswith(".jpg") or archivo.endswith(".jpeg"):  
                    dic[archivo] = cv2.imread(ruta+'/'+archivo)
        return dic


    def archivosColores(self, rutas):
        dic = {}
        for ruta in rutas:
            dic[ruta] = os.listdir(ruta)
        return dic
         

    def colorAlab(self, dictImagenes):
        dictImagenesLab = {}
        for clave, imagen in dictImagenes.items():
            dictImagenesLab[clave] = cv2.cvtColor(imagen, cv2.COLOR_BGR2LAB)
        return dictImagenesLab


    def calcularTamañoBloque(self, lab_img1, dictColores, keyCr):
        num_blocks_x = 4
        num_blocks_y = 4
        for keyCo, lab_img2 in dictColores.items():
            block_size_x = int(lab_img1.shape[1] / num_blocks_x)
            block_size_y = int(lab_img1.shape[0] / num_blocks_y)
            color_meansA = []
            color_meansB = []
            for i in range(num_blocks_y):
                for j in range(num_blocks_x):
                    block_start_x = j * block_size_x
                    block_start_y = i * block_size_y
                    block_end_x = block_start_x + block_size_x
                    block_end_y = block_start_y + block_size_y
                    block_mean1 = cv2.mean(lab_img1[block_start_y:block_end_y, block_start_x:block_end_x])
                    block_mean2 = cv2.mean(lab_img2[block_start_y:block_end_y, block_start_x:block_end_x])
                    if len(color_meansA) == len(color_meansB):
                        color_meansA.append((block_mean1[0], block_mean1[1], block_mean1[2]))
                        color_meansB.append((block_mean2[0], block_mean2[1], block_mean2[2]))
            if str(keyCo+'/'+str(keyCr)) in self.color_means.get(keyCr, {}):
                self.color_means[keyCr][str(keyCo+'/'+str(keyCr))].append([color_meansA, color_meansB])
            else:
                self.color_means.setdefault(keyCr, {})[str(keyCo+'/'+str(keyCr))] = [color_meansA, color_meansB]


    def diferencia(self, color_meansA, color_meansB):
        differences = []
        for i in range(len(color_meansA)):
            differences.append(self.delta_e_2000(color_meansA[i], color_meansB[i]))
        # Calcular el promedio de todas
        average_difference = sum(differences) / len(differences)
        return average_difference
    

    def obtenerMenorDiferencia(self, dictVals):
        dicc = {}
        for k, valDict in dictVals.items():
            for k1 in valDict.keys():
                dicc[k] = {k1: min(valDict.values())}
        return dicc

    def main(self):
        rutaImgCrop = './crop/'
        carpetasColores = os.listdir('./colores/')
        rutaColores = self.getRutaColores(carpetasColores)
        dictImgColores = self.archivosColores(rutaColores)
        dictImgsColores = {}
        for ruta in dictImgColores.keys():
            dictImgsColores[ruta] = self.leerColores(ruta+'/')
        dictImgsCrop = self.leerImgs(rutaImgCrop)
        dictImgCropLab = self.colorAlab(dictImgsCrop)
        dictImgColoresLab = {}
        for key, value in dictImgsColores.items():
            dictImgColoresLab[key] = self.colorAlab(value)
        i = 0
        for k1, valCrop in dictImgCropLab.items():
            for k2, valueColores in dictImgColoresLab.items():
                if k1.startswith(str(i)) and k2.endswith(str(i)):
                    self.calcularTamañoBloque(valCrop, valueColores, i)
            i += 1
        dicDiferencias = {}
        val = 0
        for key, valDict in self.color_means.items():
            for k, valMeans in valDict.items():
                dicDiferencias.setdefault(str(val), {})[k] = self.diferencia(valMeans[0], valMeans[1])
            val+=1
        print(dicDiferencias)
        dictMenorDif = self.obtenerMenorDiferencia(dicDiferencias)
        print(dictMenorDif)

if __name__ == '__main__':
    f = DiferenciaColores()
    f.main()





    # >>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
