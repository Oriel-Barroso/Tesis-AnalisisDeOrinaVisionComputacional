import cv2 
import numpy as np 
import os 


ruta = "./imagenes2"
# obtenemos una lista con los nombres de los archivos en la ruta especificada
archivos = os.listdir(ruta)
# iteramos sobre cada archivo en la lista
for i in range(0, len(archivos)):
    #Load an image
    if archivos[i].endswith(".jpg") or archivos[i].endswith(".jpeg"):
        img = cv2.imread(ruta+"/"+archivos[i])
        width = 600
        height = 600
        dim = (width, height)
        # Redimensionar la imagen
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        # Convert the image to grayscale 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to reduce noise (difumina el ruido de alta frecuencia - todo lo que es el fondo)
        blurred = cv2.medianBlur(gray, 5, 0)
        # create a binary thresholded image on hue between red and yellow
        thresh = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        # Perform Canny edge detection ()
        edges = cv2.Canny(blurred, 50, 150) 
        # Find contours in the edges image 
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        # Iterate over each contour 
        for contour in contours:
            # Approximate the contour to a polygon 
            polygon = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True) 
            # Check if the polygon has 4 sides 
            if len(polygon) == 4: 
                # Draw the rectangle on the image 
                x, y, w, h = cv2.boundingRect(polygon) 
                cropped_img = img[y:y+h, x:x+w]
                cv2.imwrite("imagen_rec"+str(i)+".jpg", cropped_img)
                cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2) 
        # Show the result 
        cv2.imshow("Result", img) 
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 

    # labeled - etiquetar con (labelimage) - pasar a entrenamiento - 