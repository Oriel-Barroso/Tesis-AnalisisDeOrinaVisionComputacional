# <<<<<<< HEAD
# version https://git-lfs.github.com/spec/v1
# oid sha256:c0a8965b4b3505348233c002839c152dbb6fd6f94725f3caed57bc38874980c9
# size 2452
# =======
import cv2
import os
import numpy as np
import colour


class DiferenciaColores():
    def __init__(self):
        self.color_means = {}
        self.imgColores = {}
        self.menorDiferencia = {}
        self.resultadoFinal = []
        self.resultados = {
            'sg1': 'La densidad relativa tiene un valor de: 1.000',
            'sg2': 'La densidad relativa tiene un valor de: 1.005',
            'sg3': 'La densidad relativa tiene un valor de: 1.010',
            'sg4': 'La densidad relativa tiene un valor de: 1.015',
            'sg5': 'La densidad relativa tiene un valor de: 1.020',
            'sg6': 'La densidad relativa tiene un valor de: 1.025',
            'sg7': 'La densidad relativa tiene un valor de: 1.030',
            'ph1': 'El pH tiene un valor de: 5',
            'ph2': 'El pH tiene un valor de: 6',
            'ph3': 'El pH tiene un valor de: 7',
            'ph4': 'El pH tiene un valor de: 8',
            'ph5': 'El pH tiene un valor de: 9',
            'leu1': 'Los leucocitos tienen un valor: negativo',
            'leu2': 'Los leucocitos tienen un valor de: 1 + ~ 10-25',
            'leu3': 'Los leucocitos tienen un valor de: 2 + ~ 75',
            'leu4': 'Los leucocitos tienen un valor de: 1 + 500 Leu/μL',
            'nit1': 'El nitrito tiene un valor: negativo',
            'nit2': 'El nitrito tiene un valor:positivo',
            'pro1': 'La proteina tiene un valor: negativo',
            'pro2': 'La proteina tiene un valor de: 1 + 30 (0,3)',
            'pro3': 'La proteina tiene un valor de: 2 + 100 (1)',
            'pro4': 'La proteina tiene un valor de: 3 + 500 mg/dL (5 g/L)',
            'glu1': 'La glucosa tiene un valor: normal',
            'glu2': 'La glucosa tiene un valor de: 1 + 50 (2,8)',
            'glu3': 'La glucosa tiene un valor de: 2 + 100 (5,5)',
            'glu4': 'La glucosa tiene un valor de: 3 + 300 (17)',
            'glu5': 'La glucosa tiene un valor de: 4 + 1000 mg/dL (56 mmol/L)',
            'ket1': 'Los cuerpos cetonicos tienen un valor: negativo',
            'ket2': 'Los cuerpos cetonicos tienen un valor de: 1 + 10',
            'ket3': 'Los cuerpos cetonicos tienen un valor de: 2 + 50',
            'ket4': 'Los cuerpos cetonicos tienen un valor de: 3 + 150 mg/dL (15 mmol/L)',
            'ubg1': 'El urobilinogeno tiene un valor: normal',
            'ubg2': 'El urobilinogeno tiene un valor de: 1 + 1 (17)',
            'ubg3': 'El urobilinogeno tiene un valor de: 2 + 4 (68)',
            'ubg4': 'El urobilinogeno tiene un valor de: 3 + 8 (135)',
            'ubg5': 'El urobilinogeno tiene un valor de: 4 + 12 mg/dL (203 μmol/L)',
            'bil1': 'La bilirruina tiene un valor: negativo',
            'bil2': 'La bilirruina tiene un valor de: 1+',
            'bil3': 'La bilirruina tiene un valor de: 2+',
            'bil4': 'La bilirruina tiene un valor de: 3+',
            'ery1': 'La sangre tiene un valor: negativo',
            'ery2': 'La sangre tiene un valor de: 1 + ~ 5-10',
            'ery3': 'La sangre tiene un valor de: 2 + ~ 25',
            'ery4': 'La sangre tiene un valor de: 3 + ~ 50',
            'ery5': 'La sangre tiene un valor de: 4 + ~ 250 Ery/uL',
            'hb1': 'La sangre tiene un valor de: 1 + ~ 10',
            'hb2': 'La sangre tiene un valor de: 2 + ~ 25',
            'hb3': 'La sangre tiene un valor de: 3 + ~ 50',
            'hb4': 'La sangre tiene un valor de: 4 + ~ 250 Ery/uL',
        }

    def leerImgs(self, ruta):
        archivos = os.listdir(ruta)
        archivos.sort()
        dicc = {}
        for archivo in archivos:
            if archivo.endswith(".jpg") or archivo.endswith(".jpeg"):
                dicc[archivo] = cv2.imread(ruta+'/'+archivo)
        return dicc

    def archivosColores(self, rutas):
        dic = {}
        for ruta in rutas:
            dic[ruta] = os.listdir(ruta)
        return dic

    def getRutaColores(self, carpetas):
        lista = []
        for i in range(0, len(carpetas)):
            lista.append('./colores/'+carpetas[i])
        return lista

    def leerColores(self, ruta):
        archivos = os.listdir(ruta)
        for archivo in archivos:
            if archivo.endswith(".jpg") or archivo.endswith(".jpeg"):
                idx = archivo.index('.')
                self.imgColores[archivo[:idx] +
                                ruta[:len(ruta)-1]] = cv2.imread(ruta+'/' +
                                                                 archivo)

    def calculate_delta_eitp(self, image1, image2):
        size = (min(image1.shape[1], image2.shape[1]),
                min(image1.shape[0], image2.shape[0]))
        image1 = cv2.resize(image1, size)
        # Convertir a ambas imagenes al mismo tamaño
        image2 = cv2.resize(image2, size)
        x1 = cv2.cvtColor(image1, cv2.COLOR_BGR2XYZ)
        x2 = cv2.cvtColor(image2, cv2.COLOR_BGR2XYZ)
        ictcp1 = colour.models.rgb.XYZ_to_ICtCp(x1/100)
        ictcp2 = colour.models.rgb.XYZ_to_ICtCp(x2/100)
        s = colour.difference.delta_E_ITP(ictcp1, ictcp2)
        d = colour.difference.power_function_Huang2015(s)
        avg_delta_eitp1 = np.mean(d)
        return avg_delta_eitp1

    def obtenerMenorDiferencia(self, dictVals):
        valorMin = min(dictVals.values())
        for k, valDict in dictVals.items():
            if valorMin in [valDict]:
                self.menorDiferencia[k[k.index(
                    '/')+1:k.index('.')]] = {k: valorMin}

    def obtenerResultado(self, val):
        for k, v in self.resultados.items():
            for k1, v1 in val.items():
                if k == k1[:k1.index('/')]:
                    self.resultadoFinal.append(v)

    def main(self):
        rutaImgCrop = './crop/'
        carpetasColores = os.listdir('./colores/')
        rutaColores = self.getRutaColores(carpetasColores)
        dictImgColores = self.archivosColores(rutaColores)
        for ruta in dictImgColores.keys():
            self.leerColores(ruta+'/')
        dictImgsCrop = self.leerImgs(rutaImgCrop)
        dicDiferencias = {}
        val = 0
        for k, valMeans in dictImgsCrop.items():
            for k2, valDict in self.imgColores.items():
                if k.startswith(str(val)) and k2.endswith(str(val)):
                    dicDiferencias.setdefault(str(val), {})[k2[:k2.index(
                        '.')]+'/'+k] = self.calculate_delta_eitp(valMeans,
                                                                 valDict)
            val += 1
        for v in dicDiferencias.values():
            self.obtenerMenorDiferencia(v)
        print(self.menorDiferencia)
        for k, v in self.menorDiferencia.items():
            self.obtenerResultado(v)
        print('\n\n\n')
        print(self.resultadoFinal)


if __name__ == '__main__':
    f = DiferenciaColores()
    f.main()

    # >>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
