#import modules
import cv2
import numpy as np

#Capture video through default camera
#cap = cv2.VideoCapture(0)
#while True:_, img = cap.read()

img = cv2.imread("testImage.png",1)
imgCopy = img.copy()

#Determine the size of the image
imgHeight = np.size(imgCopy,0)
imgWidth = np.size(imgCopy, 1)
xCenter = int(imgWidth/2)
yCenter = int(imgHeight/2)
xLimitLeft = xCenter - int(0.40*imgWidth)
xLimitRight = xCenter + int(0.40*imgWidth)
yLimit = int(0.25*imgHeight)

#Convert img frame from BGR to HSV
imgHSV = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2HSV)

#deflining the range of green color
woodLower = np.array([9,16,163], np.uint8)
woodUpper = np.array([29,36,243], np.uint8)
greenLower = np.array([22,80,40],np.uint8)
greenUpper = np.array([60,255,255],np.uint8)

#Filter out other colours, only show green colour
greenMask = cv2.inRange(imgHSV, greenLower, greenUpper)

#Wood mask
woodMask = cv2.inRange(imgHSV, woodLower, woodUpper)

#Morphological Transformation
kernelOpen = np.ones((8,8),"uint8")
kernelClose = np.ones((15,15),"uint8")
kernelOpen2 = np.ones((8,8),"uint8")
maskOpenMorph = cv2.morphologyEx(greenMask | woodMask, cv2.MORPH_OPEN, kernelOpen)
maskCloseMorph = cv2.morphologyEx(greenMask | woodMask, cv2.MORPH_CLOSE, kernelClose)
maskOpenMorph2 = cv2.morphologyEx(maskCloseMorph, cv2.MORPH_OPEN, kernelOpen2)

#Find Contours 
contours,hierarchy = cv2.findContours(maskOpenMorph2.copy(),
                         mode = cv2.RETR_EXTERNAL,
                         method = cv2.CHAIN_APPROX_NONE)

#cv2.drawContours(imgCopy, contours, -1, (0,0,255), thickness = 2)

#Bound the contours if contours are large enough
for i in range(len(contours)):
     area = cv2.contourArea(contours[i])
     if(area > 250):
          x,y,w,h = cv2.boundingRect(contours[i])
          cv2.rectangle(imgCopy, (x,y), (x+w, y+h), (255,0,0), 2)

''' pseudo code for arduino command         
          if(y >= yLimit):
               if(((x>xLimitLeft) || (x+w > xLimitLeft)) && ((x<xCenter) || (x+w < xCenter))):
                    # tell arduino to make a slight turn to right
               else if(((x<xLimitRight) || (x+w < xLimitRight)) && ((x>xCenter) || (x+w > xCenter))):
                    # tell arduino to make a slight turn to left
'''         

cv2.line(imgCopy, (0,yLimit), (imgWidth,yLimit), (255,255,255), 2) # top limit
cv2.line(imgCopy, (xLimitLeft, 0), (xLimitLeft, imgHeight), (255,255,255), 2) # left limit
cv2.line(imgCopy, (xLimitRight,0), (xLimitRight, imgHeight), (255,255,255), 2) # right limit


cv2.imshow("Image in test", imgCopy)
cv2.imshow("mask", greenMask | woodMask)
cv2.imshow("Morphology Opening", maskOpenMorph)
cv2.imshow("Morphology second Opening", maskOpenMorph2)
cv2.waitKey(0)

#print("H = "+str(imgHeight) + "\nWidth = " + str(imgWidth))

'''
#Tracking Colour (Yellow) 
(_,contours,hierarchy)=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
     for pic, contour in enumerate(contours):
              area = cv2.contourArea(contour)
              if(area>300):
                   x,y,w,h = cv2.boundingRect(contour)     
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)

'''