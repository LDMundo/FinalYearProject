#import modules
import cv2
import numpy as np

#Capture video through default camera
#cap = cv2.VideoCapture(0)
#while True:_, img = cap.read()

img = cv2.imread("testImage.png",1)
imgCopy = img.copy()

#Convert img frame from BGR to HSV
imgHSV = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2HSV)

#defining the range of green color
greenLower = np.array([22,80,40],np.uint8)
greenUpper = np.array([60,255,255],np.uint8)

#Filter out other colours, only show green colour
greenMask = cv2.inRange(imgHSV, greenLower, greenUpper)

#Morphological Transformation
kernelOpen = np.ones((8,8),"uint8")
kernelClose = np.ones((20,20),"uint8")
maskOpenMorph = cv2.morphologyEx(greenMask, cv2.MORPH_OPEN, kernelOpen)
maskCloseMorph = cv2.morphologyEx(greenMask, cv2.MORPH_CLOSE, kernelClose)

#Find Contours 
contours,hierarchy = cv2.findContours(maskCloseMorph.copy(),
                         mode = cv2.RETR_EXTERNAL,
                         method = cv2.CHAIN_APPROX_NONE)

#cv2.drawContours(imgCopy, contours, -1, (0,0,255), thickness = 2)

for i in range(len(contours)):
     area = cv2.contourArea(contours[i])
     if(area > 300):
          x,y,w,h = cv2.boundingRect(contours[i])
          cv2.rectangle(imgCopy, (x,y), (x+w, y+h), (255,0,0), 2)
          print("(" + str(x) + "," + str(y) + ")    (" + str(x+w) + "," + str(y+h) + ")")


imgHeight = np.size(imgCopy,0)
imgWidth = np.size(imgCopy, 1)
print("H = "+str(imgHeight) + "\nWidth = " + str(imgWidth))
cv2.imshow("Image in test", imgCopy)
cv2.imshow("mask", greenMask)
cv2.imshow("Morphology Opening", maskOpenMorph)
cv2.imshow("Morphology Closing", maskCloseMorph)
cv2.waitKey(0)



'''
#Tracking Colour (Yellow) 
(_,contours,hierarchy)=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
     for pic, contour in enumerate(contours):
              area = cv2.contourArea(contour)
              if(area>300):
                   x,y,w,h = cv2.boundingRect(contour)     
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)

#Display results
img = cv2.flip(img,1)
cv2.imshow("Yellow",res)
'''