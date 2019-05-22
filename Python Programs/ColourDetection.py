'''
     Object tracking code for coloured objects 
     This code will be used as an object detection tool for robotic Rotavator
     The code  is currently detecting green, and plywood colour
     
     By: Lloyd Mundo
     Last Modified: 01/05/2019
'''
#import modules
import cv2
import numpy as np

#Capture video through default camera


#cap = cv2.VideoCapture(0)
#_, img = cap.read()
#img = cv2.imread("saturated.jpg",1)


#img = cv2.imread("saturated.jpg",1)

#img = cv2.imread("testImage.JPG", 1)
imgCopy = img.copy()

#Determine the size of the image
imgHeight = np.size(imgCopy, 0)
imgWidth = np.size(imgCopy, 1)
xCenter = int(imgWidth/2)
yCenter = int(imgHeight/2)
xLimitLeft = xCenter - int(0.40*imgWidth)
xLimitRight = xCenter + int(0.40*imgWidth)
yLimit = int(0.25*imgHeight)


#Convert img frame from BGR to HSV
imgHSV = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2HSV) 
'''
(h, s, v) = cv2.split(imgHSV)
h= h+15
h = np.clip(h, 0, 255)
s = s*2
s = np.clip(s, 0, 255)
imgHSV = cv2.merge([h, s, v])
'''

#deflining the range of green color
#woodLower = np.array([9, 16, 163], np.uint8)        #lower range of wood colour
##woodUpper = np.array([29, 36, 243], np.uint8)       #upper range of wood colour
greenLower = np.array([34,  112,  75], np.uint8)       #lower range of green colour
greenUpper = np.array([54, 255, 255], np.uint8)     #upper range of wood colour

#Filter out other colours, only show green colour
greenMask = cv2.inRange(imgHSV, greenLower, greenUpper)
#Wood mask
woodMask = cv2.inRange(imgHSV, woodLower, woodUpper)

#Morphological Transformation
kernelOpen = np.ones((5,5), "uint8")
kernelClose = np.ones((15,15), "uint8")
maskOpenMorph = cv2.morphologyEx(greenMask, cv2.MORPH_OPEN, kernelOpen)
maskCloseMorph = cv2.morphologyEx(maskOpenMorph, cv2.MORPH_CLOSE, kernelClose)
#Find Contours 
contours, _ = cv2.findContours(maskCloseMorph.copy(), mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE)

#Bound the contours if contours are large enough
for i in range(len(contours)):
     area = cv2.contourArea(contours[i])
     if(area > 250):
          x,y,w,h = cv2.boundingRect(contours[i])
          cv2.rectangle(imgCopy, (x,y), (x+w, y+h), (255,0,0), 2)
     #print("rectangle " + str(i) + "   " + str(x) + "," + str(y))
''' pseudo code for arduino command         
          if(y+h >= yLimit):
               if(((x>xLimitLeft) || (x+w > xLimitLeft)) && ((x<xCenter) || (x+w < xCenter))):
                    # tell arduino to make a slight turn to right
               else if(((x<xLimitRight) || (x+w < xLimitRight)) && ((x>xCenter) || (x+w > xCenter))):
                    # tell arduino to make a slight turn to left
'''         

cv2.line(img, (0,yLimit), (imgWidth,yLimit), (255,255,255), 2) # top limit
cv2.line(img, (xLimitLeft, 0), (xLimitLeft, imgHeight), (255,255,255), 2) # left limit
cv2.line(img, (xLimitRight,0), (xLimitRight, imgHeight), (255,255,255), 2) # right limit


cv2.imshow("Image in test", img)
cv2.imshow("mask", greenMask)
cv2.imshow("Morphology Opening", maskOpenMorph)
cv2.imshow("Morphology Closing", maskCloseMorph)
cv2.waitKey(10)
#print("H = "+str(imgHeight) + "\nWidth = " + str(imgWidth))
