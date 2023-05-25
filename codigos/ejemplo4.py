<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:781f94f3f3de714deb66f6c2c3d7827020cd8a803b5d6e0e0293e7cc5aeb8d7d
size 1027
=======
import cv2
import numpy as np



img = cv2.imread('imagen17.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

# create a binary thresholded image on hue between red and yellow
thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]

# apply morphology
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15))
clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# get external contours
contours = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

result1 = img.copy()
result2 = img.copy()
for c in contours:
    cv2.drawContours(result1,[c],0,(0,0,0),2)



cv2.imshow("result1", result1)
cv2.waitKey(0)
cv2.destroyAllWindows()
>>>>>>> dd70e7b7faf0d5343b65a4259fa25ca263dd82da
