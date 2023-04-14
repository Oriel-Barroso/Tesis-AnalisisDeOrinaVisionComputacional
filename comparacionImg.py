import cv2
import numpy as np

# Lee la imagen
img = cv2.imread(r"C:\Users\Oriel\Documents\testIA\testIA\imagen18.jpg")
# Obtiene las dimensiones de la imagen
height, width = img.shape[:2]

# Define las regiones de interés (ROI)
start_roi = img[0:height, 0:300]
end_roi = img[0:height, width-300:width]
# Calculate the standard deviation of the color channels
std_dev_start = np.std(start_roi, axis=(0,1))

# Check if the image is completely white or has color interference
if std_dev_start[0] < 30 and std_dev_start[1] < 30 and std_dev_start[2] < 30:
    print("The image is completely white")
    rotated_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
else:
    print("The image has color interference")
    rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)


# Muestra la imagen de diferencia
#cv2.imwrite("rotated_img.jpg", rotated_img)
cv2.imshow('Difference', rotated_img)
cv2.waitKey(0)
cv2.destroyAllWindows()