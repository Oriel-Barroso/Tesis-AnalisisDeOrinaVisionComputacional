import cv2

# Cargar la imagen y convertirla a escala de grises
img = cv2.imread('imagen5.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar el filtro de Canny para detectar los bordes de la imagen
edges = cv2.Canny(gray, 100, 200)

# Buscar los contornos de la imagen
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar los contornos para encontrar el rectángulo y generar una nueva imagen de cada rectángulo recortado
rectangles = []
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
        area = cv2.contourArea(cnt)
        if area > 1000:
            x,y,w,h = cv2.boundingRect(cnt)
            # Verificar si el rectángulo ya se encuentra en la lista de rectángulos
            if (x,y,w,h) not in rectangles:
                # Recortar el rectángulo de la imagen original y guardar la nueva imagen en un archivo
                roi = img[y:y+h, x:x+w]
                cv2.imwrite('rectangulo_{}.jpg'.format(len(rectangles)), roi)
                rectangles.append((x,y,w,h))