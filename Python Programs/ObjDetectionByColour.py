'''
     Object tracking code for coloured objects 
     This code will be used as an object detection tool for robotic Rotavator
     The code  is currently detecting green, and plywood colour
     
     By: Lloyd Mundo
     Last Modified: 06/05/2019
'''
#import modules
import cv2
import numpy as np
import time
import serial

#initialise and opens the serial communication
ser = serial.Serial(
        port='/dev/serial0',            #port
        baudrate=9600,                  #baud rate is the same as arduino
        parity=serial.PARITY_NONE,      #no parity
        stopbits=serial.STOPBITS_ONE,   #defining stop bit as 1
        bytesize=serial.EIGHTBITS,      #size of incoming byte
        timeout=0.3                     #timeout
)

#Global Variables
#cam = cv2.VideoCapture(0)

#function to return mask 
def extractMask(img):
    imgCopy = img.copy()
    #Convert img frame from BGR to HSV
    imgHSV = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2HSV)

    #deflining the range of colours 
    woodLower = np.array([9, 16, 163], np.uint8)
    woodUpper = np.array([29, 36, 243], np.uint8)
    greenLower = np.array([22, 80, 40], np.uint8)
    greenUpper = np.array([60, 255, 255], np.uint8)

    #Filter out other colours, only show green colour
    greenMask = cv2.inRange(imgHSV, greenLower, greenUpper)
    #Wood mask
    woodMask = cv2.inRange(imgHSV, woodLower, woodUpper)

    #Morphological Transformation
    kernelOpen = np.ones((5,5), "uint8")
    kernelClose = np.ones((15,15), "uint8")
    maskOpenMorph = cv2.morphologyEx(greenMask | woodMask, cv2.MORPH_OPEN, kernelOpen)
    maskCloseMorph = cv2.morphologyEx(maskOpenMorph, cv2.MORPH_CLOSE, kernelClose)

    return(maskCloseMorph)


while True:
    while ser.inWaiting():
        message = ser.read(3)
        if (mesaage..decode('utf-8') == "req"):
            #_, frame = cam.read()
            frame = cv2.imread("testImage.jpg",1)
            #Determine the size of the image
            imgHeight = np.size(frame, 0)
            imgWidth = np.size(frame, 1)

            #Limits 
            xCenter = int(imgWidth/2)
            yCenter = int(imgHeight/2)
            xLimitLeft = xCenter - int(0.40*imgWidth)
            xLimitRight = xCenter + int(0.40*imgWidth)
            yLimit = int(0.25*imgHeight)

            mask = extractMask(frame)
            contours, hierarchy = cv2.findContours(mask.copy(), mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE)
            for i in range(len(contours)):
                area = cv2.contourArea(contours[i])
                if(area > 250):
                    x,y,w,h = cv2.boundingRect(contours[i])
                    cv2.rectangle(mask.copy(), (x,y), (x+w, y+h), (255,0,0), 2)
                    print("rectangle " + str(i) + "   " + str(x) + "," + str(y))

                    if(y+h >= yLimit):
                        if(((x>xLimitLeft) || (x+w > xLimitLeft)) && ((x<xCenter) || (x+w < xCenter))):
                            ser.write('turnRight'.encode('utf-8'))
                            ser.flush() 
                        else if(((x<xLimitRight) || (x+w < xLimitRight)) && ((x>xCenter) || (x+w > xCenter))):
                            ser.write('turnLeft'.encode('utf-8'))
                            ser.flush() 
                    else if ((y+h <= yLimit) && (y+h <= yLimit-int(0.5*yLimit)) ):
                        ser.write('reverse'.encode('utf-8'))
                        ser.flush() 
                else:
                    ser.write('noObject'.encode('utf-8'))
                    ser.flush() 



