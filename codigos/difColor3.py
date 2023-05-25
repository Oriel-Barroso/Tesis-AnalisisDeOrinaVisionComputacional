import cv2
import numpy as np


def ColorDistance(rgb1, rgb2):
    diff = cv2.absdiff(rgb1, rgb2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    return np.mean(gray)


i1 = cv2.imread('./crop/0.jpg')
i2 = cv2.imread('./colores/0/hb1.jpeg')

# Redimensionar las imágenes para que tengan el mismo tamaño
i1 = cv2.resize(i1, (i2.shape[1], i2.shape[0]))

print(ColorDistance(i1, i2))
