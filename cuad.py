import cv2

# Cargar la imagen y convertirla a escala de grises
img = cv2.imread('imagen7.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar el filtro de Canny para detectar los bordes de la imagen
edges = cv2.Canny(gray, 100, 200)

# Buscar los contornos de la imagen
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

# Filtrar los contornos para encontrar los cuadrados y generar una nueva imagen de cada cuadrado recortado
i = 0
cuads = []
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
        area = cv2.contourArea(cnt)
        if area > 1000:
            # Verificar que el contorno es un cuadrado
            x,y,w,h = cv2.boundingRect(cnt)
            if (x,y,w,h) not in cuads:
                if abs(w-h) < 50: # Se considera cuadrado si la diferencia entre ancho y alto es menor a 50 pixels
                    # Recortar el cuadrado de la imagen original y guardar la nueva imagen en un archivo
                    roi = img[y:y+h, x:x+w]
                    cv2.imwrite('cuadrado_{}.jpg'.format(i), roi)
                    cuads.append((x,y,w,h))
                    i += 1