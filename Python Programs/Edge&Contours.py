#Import packages
import cv2
import numpy as np
from matplotlib import pyplot as plt
import easygui

#open (I)mage from (f)ile using dialog 
#f = easygui.fileopenbox()
I = cv2.imread('download.jpg', 1)

#Convert image to (G)reyscale
G = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

#Obtain (E)dges using Canny function
E = cv2.Canny(G, threshold1=100, threshold2=150)

#Using adaptive thresholding to obtain edges
B = cv2.adaptiveThreshold(G, maxValue=255,
        adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType = cv2.THRESH_BINARY,
        blockSize = 5, C = 15)


#Find contours



plt.subplot(2,2,1),plt.imshow(G, cmap='gray')
plt.subplot(2,2,2),plt.imshow(E, cmap='gray')
plt.subplot(2,2,3),plt.imshow(B, cmap='gray')
plt.show()
