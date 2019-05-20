
'''
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.image_effect = 'denoise'
camera.image_effect = 'colorbalance'
camera.image_effect = 'colorpoint'
camera.image_effect = 'saturation'
sleep(30)
camera.stop_preview()
'''

import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while True:
    _, frame = cam.read();
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #cv2.imshow("Frame", frame)
    imgHSV = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV) 
    (h, s, v) = cv2.split(imgHSV)
    h = h+15
    h = np.clip(h, 0, 255)
    s = s+30
    s = np.clip(s, 0, 255)
    imgHSV = cv2.merge([h, s, v])
    
    imgBGR = cv2.cvtColor(imgHSV, cv2.COLOR_HSV2BGR)
    #cv2.imwrite("saturated.jpg", imgBGR)
    cv2.imshow("img saturated", imgBGR)
    key = cv2.waitKey(1)
    if key == 2:
        break



'''
_, frame = cam.read()
cv2.imshow("Frame", frame)
cv2.imwrite("frame.jpg", frame)
'''
