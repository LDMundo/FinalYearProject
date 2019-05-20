'''
     Object tracking code for coloured objects 
     This code will be used as an object detection tool for robotic Rotavator
     The code  is currently detecting green, and plywood colour
     
     By: Lloyd Mundo
     Last Modified: 20/05/2019
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

#camera
cam = cv2.VideoCapture(0)

#function to return mask 
def extractMask(img):
    imgCopy = img.copy()
    #Convert img frame from BGR to HSV
    imgHSV = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2HSV) 
    '''
    (h, s, v) = cv2.split(imgHSV)   #extract the HSV values individually
    h = h+15                        #increase H channel
    h = np.clip(h, 0, 255)          #ensure it is within 0 and 255
    s = s*2                         #increase Saturation channel
    s = np.clip(s, 0, 255)          #ensure it is within 0 and 255
    imgHSV = cv2.merge([h, s, v])   #merge the changes
    '''
    
    #deflining the range of colours [H, S, V]
    woodLower = np.array([9, 16, 163], np.uint8)        #lower range of wood colour
    woodUpper = np.array([29, 36, 243], np.uint8)       #upper range of wood colour
    greenLower = np.array([165,  44,  45], np.uint8)    #lower range of green colour
    greenUpper = np.array([175, 61, 120], np.uint8)     #upper range of wood colour

    #All colours within range are turned to white (255), otherwise, black (0)
    #green colour mask
    greenMask = cv2.inRange(imgHSV, greenLower, greenUpper)  
    #Wood mask
    woodMask = cv2.inRange(imgHSV, woodLower, woodUpper)

    #Morphological Transformation
    kernelOpen = np.ones((5,5), "uint8")    #structuring element for morphology opening
    kernelClose = np.ones((15,15), "uint8") #structuring element for morphology closing
    maskOpenMorph = cv2.morphologyEx(greenMask | woodMask, cv2.MORPH_OPEN, kernelOpen)  #morphology opening
    maskCloseMorph = cv2.morphologyEx(maskOpenMorph, cv2.MORPH_CLOSE, kernelClose)      #morphology closing

    return(maskCloseMorph)  # retun the noiseless mask


while True:
    while ser.inWaiting(): #execute when data is available from arduino
        message = ser.read(7)   #reads 7 bytes of data
        
        if (message.decode('utf-8') == "request"):  # check if the message decoded is "request"
            _, frame = cam.read()                   #read a frame/image off the camera
            #frameCopy = cv2.imread("testImage.JPG",1)
            frameCopy = frame.copy()                #make a copy of the image
                        
            #Determine the size of the image
            imgHeight = np.size(frameCopy, 0)       #takes the height of the frame
            imgWidth = np.size(frameCopy, 1)        #takes the width of the frame

            #Limits 
            xCenter = int(imgWidth/2)                   #x coordinate of the centre of the frame
            yCenter = int(imgHeight/2)                  #y coordinate of the centre of the frame
            xLimitLeft = xCenter - int(0.40*imgWidth)   #left boundary of the frame
            xLimitRight = xCenter + int(0.40*imgWidth)  #right boundary of the frame
            yLimit = int(0.25*imgHeight)                #top boundaary of the frame

            mask = extractMask(frame.copy())            #obtain the mask containing only the region of interest
            _, contours, _= cv2.findContours(mask, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE) #extract contours
            closestYplusH = 0   # cloest rectangle's bottom y coordinate    
            xOfInterest = 0     # x coordinate of the closest bounnding rectangle
            yOfInterest = 0     # y coordinate of the closest bounnding rectangle
            wOfInterest = 0     # width of the closest bounnding rectangle
            hOfInterest = 0     # heigh of the closest bounnding rectangle      
            for i in range(len(contours)):              #iterates through all the contours found
                area = cv2.contourArea(contours[i])     #takes the area of the indexed contour
                if(area > 250):                         #if the area of the contour is greater than 250 px^2
                    x,y,w,h = cv2.boundingRect(contours[i]) #enclosed the contour with a bounding rectangle
                    cv2.rectangle(frameCopy, (x,y), (x+w, y+h), (255,0,0), 2)
                    #print("rectangle " + str(i) + "   " + str(x) + "," + str(y))
                    
                    #check if the bottom y coordinate is greater than the current closet rectangle
                    if y+h > closestYplusH:
                        closestYplusH = y+h
                        xOfInterest = x
                        yOfInterest = y
                        wOfInterest = w
                        hOfInterest = h 

            if closestYplusH > 0:
                if closestYplusH >= yLimit:
                    xplusw = xOfInterest + wOfInterest
                    if (xOfInterest>xLimitLeft or xplusw>xLimitLeft) and (xOfInterest<xCenter or xplusw<xCenter):
                        print("turnRight\n")
                        ser.write('turnRight'.encode('utf-8'))
                        ser.flush() 
                            
                    elif (xOfInterest<xLimitRight or xplusw<xLimitRight) and (xOfInterest>xCenter or xplusw>xCenter):
                        print("turnLeft\n")
                        ser.write('turnLeft'.encode('utf-8'))
                        ser.flush()                                                              
                elif (closestYplusH <= yLimit) and (closestYplusH >= yLimit-int(0.5*yLimit)):
                        print("reverse\n")
                        ser.write('reverse'.encode('utf-8'))
                        ser.flush() 
            else:
                print("noObject\n")
                ser.write('noObject'.encode('utf-8'))
                ser.flush() 
        else:
            ser.write('invalid'.encode('utf-8'))
            ser.flush()
            print("invalid\n")


