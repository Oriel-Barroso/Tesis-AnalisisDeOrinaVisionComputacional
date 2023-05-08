import os
import re


ruta = r"/mnt/c/Users/Admin/Documents/testIA/yolov7/train/labels"
archivos = os.listdir(ruta)
archivos_txt = [arc for arc in archivos if re.match(r'.+.txt', arc)]
for arc in archivos_txt:
    ruta1 = os.path.join(ruta, arc)
    with open(ruta1, 'r') as f:
        lines = f.readlines()
        with open(ruta1, 'w') as f:
            for i, line in enumerate(lines):
                values = line.split()
                values[0] = str(0)
                f.write(" ".join(values) + "\n")
