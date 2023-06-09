import cv2
import os
import colour


class DiferenciaColores():
    def __init__(self, imagePath=''):
        self.color_means = {}
        self.imgColores = {}
        self.menorDiferencia = {}
        self.resultadoFinal = []
        self.imagePath = imagePath
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.resultados = {
            's1': 'La densidad relativa tiene un valor de: 1.000',
            's2': 'La densidad relativa tiene un valor de: 1.005',
            's3': 'La densidad relativa tiene un valor de: 1.010',
            's4': 'La densidad relativa tiene un valor de: 1.015',
            's5': 'La densidad relativa tiene un valor de: 1.020',
            's6': 'La densidad relativa tiene un valor de: 1.025',
            's7': 'La densidad relativa tiene un valor de: 1.030',
            'x1': 'El pH tiene un valor de: 5',
            'x2': 'El pH tiene un valor de: 6',
            'x3': 'El pH tiene un valor de: 7',
            'x4': 'El pH tiene un valor de: 8',
            'x5': 'El pH tiene un valor de: 9',
            'l1': 'Los leucocitos tienen un valor: negativo',
            'l2': 'Los leucocitos tienen un valor de: 1 + ~ 10-25',
            'l3': 'Los leucocitos tienen un valor de: 2 + ~ 75',
            'l4': 'Los leucocitos tienen un valor de: 3 + 500 Leu/μL',
            'n1': 'El nitrito tiene un valor: negativo',
            'n2': 'El nitrito tiene un valor:positivo',
            'p1': 'La proteina tiene un valor: negativo',
            'p2': 'La proteina tiene un valor de: 1 + 30 (0,3)',
            'p3': 'La proteina tiene un valor de: 2 + 100 (1)',
            'p4': 'La proteina tiene un valor de: 3 + 500 mg/dL (5 g/L)',
            'g1': 'La glucosa tiene un valor: normal',
            'g2': 'La glucosa tiene un valor de: 1 + 50 (2,8)',
            'g3': 'La glucosa tiene un valor de: 2 + 100 (5,5)',
            'g4': 'La glucosa tiene un valor de: 3 + 300 (17)',
            'g5': 'La glucosa tiene un valor de: 4 + 1000 mg/dL (56 mmol/L)',
            'k1': 'Los cuerpos cetonicos tienen un valor: negativo',
            'k2': 'Los cuerpos cetonicos tienen un valor de: 1 + 10',
            'k3': 'Los cuerpos cetonicos tienen un valor de: 2 + 50',
            'k4': 'Los cuerpos cetonicos tienen un valor de: 3 + 150 mg/dL (15 mmol/L)',
            'u1': 'El urobilinogeno tiene un valor: normal',
            'u2': 'El urobilinogeno tiene un valor de: 1 + 1 (17)',
            'u3': 'El urobilinogeno tiene un valor de: 2 + 4 (68)',
            'u4': 'El urobilinogeno tiene un valor de: 3 + 8 (135)',
            'u5': 'El urobilinogeno tiene un valor de: 4 + 12 mg/dL (203 μmol/L)',
            'b1': 'La bilirruina tiene un valor: negativo',
            'b2': 'La bilirruina tiene un valor de: 1+',
            'b3': 'La bilirruina tiene un valor de: 2+',
            'b4': 'La bilirruina tiene un valor de: 3+',
            'e1': 'La sangre tiene un valor: negativo',
            'e2': 'La sangre tiene un valor de: 1 + ~ 5-10',
            'e3': 'La sangre tiene un valor de: 2 + ~ 25',
            'e4': 'La sangre tiene un valor de: 3 + ~ 50',
            'e5': 'La sangre tiene un valor de: 4 + ~ 250 Ery/uL',
            'h1': 'La sangre tiene un valor de: 1 + ~ 10',
            'h2': 'La sangre tiene un valor de: 2 + ~ 25',
            'h3': 'La sangre tiene un valor de: 3 + ~ 50',
            'h4': 'La sangre tiene un valor de: 4 + ~ 250 Ery/uL',
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
            lista.append(self.current_dir+'/colores/'+carpetas[i])
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
        image2 = cv2.resize(image2, size)
        x1 = cv2.cvtColor(image1, cv2.COLOR_BGR2XYZ)
        x2 = cv2.cvtColor(image2, cv2.COLOR_BGR2XYZ)
        cam02scdA = colour.models.XYZ_to_CAM02SCD(x1)
        cam02scdB = colour.models.XYZ_to_CAM02SCD(x2)
        s = colour.difference.delta_E_CAM02SCD(cam02scdA, cam02scdB)
        avg_delta_eitp1 = s.mean()
        return avg_delta_eitp1

    def obtenerMenorDiferencia(self, dictVals):
        valorMin = min(dictVals.values())
        for k, valDict in dictVals.items():
            if valorMin in [valDict]:
                self.menorDiferencia[k[k.index(
                    '/')+1:k.index('.')]] = {k: valorMin}

    def obtenerResultado(self, val):
        for k, v in self.resultados.items():
            ka = k[0]
            k2 = k[-1]
            k3 = ka+k2
            for k1 in val.keys():
                kb = k1[:k1.index('/')]
                kc = kb[0]
                kd = kb[-1]
                ke = kc+kd
                if k3 == ke:
                    self.resultadoFinal.append(v)

    def main(self):
        rutaImgCrop = self.current_dir+'/crop/'+self.imagePath
        carpetasColores = os.listdir(self.current_dir+'/colores/')
        rutaColores = self.getRutaColores(carpetasColores)
        dictImgColores = self.archivosColores(rutaColores)
        for ruta in dictImgColores.keys():
            self.leerColores(ruta+'/')
        dictImgsCrop = self.leerImgs(rutaImgCrop)
        dicDiferencias = {}
        val = 0
        for k, valMeans in dictImgsCrop.items():
            for k2, valDict in self.imgColores.items():
                if k.startswith(str(val)) and k2[-1].startswith(str(val)):
                    dicDiferencias.setdefault(str(val), {})[k2[:k2.index(
                        '/')]+'/'+k] = self.calculate_delta_eitp(valMeans,
                                                                 valDict)
            val += 1
        for v in dicDiferencias.values():
            self.obtenerMenorDiferencia(v)
        for v in self.menorDiferencia.values():
            self.obtenerResultado(v)
        print(self.resultadoFinal)
        return self.resultadoFinal
