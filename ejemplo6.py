import cv2
import numpy as np

# Load an image
img = cv2.imread("imagen18.jpg", 0) # Load the image in grayscale

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# Calculate an adaptive threshold using Otsu's method
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

# Show the result
cv2.imshow("Result", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()