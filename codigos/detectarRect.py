<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:b6970d4fe016a237fd8eb5371d431f488bc8ee2bc414e797f273da201fe568a4
size 2395
=======
import cv2 
import numpy as np 
import os 


ruta = "./imagenes2"
# obtenemos una lista con los nombres de los archivos en la ruta especificada
archivos = os.listdir(ruta)
print(len(archivos))
# iteramos sobre cada archivo en la lista
cont = 0
for i in range(0, len(archivos)):
    #Load an image
    if archivos[i].endswith(".jpg") or archivos[i].endswith(".jpeg"):
        img = cv2.imread(ruta+"/"+archivos[i])
        width = 1000
        height = 1000
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
                heightN, widthN = cropped_img.shape[:2]
                cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)
                #cv2.imshow("Result", cropped_img) 
                #cv2.waitKey(0) 
                #cv2.destroyAllWindows()
                if heightN > 30 and widthN > 30:
                    cont+=1
                    # cv2.imshow("Result", cropped_img) 
                    # cv2.waitKey(0) 
                    # cv2.destroyAllWindows() 
                    cv2.imwrite("./imagenesREC/imagen_rec"+str(i)+".jpg", cropped_img)

        # Show the result 

    # labeled - etiquetar con (labelimage) - pasar a entrenamiento 
>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
