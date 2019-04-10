####### Import Packages #######
import cv2
import numpy as np
from matplotlib import pyplot as plt


#reads image to img in color (1), grayscale (0)
img = cv2.imread('img1.png', 0)

# cv2.imshow('figure1', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

Ix = cv2.Sobel(img, ddepth=cv2.CV_64F, dx=1, dy=0)
Iy = cv2.Sobel(img, ddepth=cv2.CV_64F, dx=0, dy=1)
Gmag, ang = cv2.cartToPolar(Ix, Iy) #cartesian form to polar form

Gmag_alt = np.sqrt(Ix*Ix + Iy*Iy)   #alternative
ang_alt = np.arctan(Iy/Ix)          #alternative

#canny thresholding allows to detect edges from gradients
E = cv2.Canny(img,threshold1=100,threshold2=200)

plt.subplot(2,3,1),plt.imshow(img,cmap = 'gray')
plt.subplot(2,3,2),plt.imshow(Ix,cmap = 'gray')
plt.subplot(2,3,3),plt.imshow(Iy,cmap = 'gray')
plt.subplot(2,3,4),plt.imshow(Gmag,cmap = 'gray')
plt.subplot(2,3,5),plt.imshow(ang,cmap = 'gray')
plt.subplot(2,3,6),plt.imshow(E,cmap = 'gray')

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
