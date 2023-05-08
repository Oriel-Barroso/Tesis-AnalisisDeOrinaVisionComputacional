import cv2
import numpy as np

# Load an image
img = cv2.imread(r"C:\Users\Admin\Documents\imgEnt\imagen_113.jpg", 0) # Load the image in grayscale

height, width = img.shape[:2]

print(height, width)