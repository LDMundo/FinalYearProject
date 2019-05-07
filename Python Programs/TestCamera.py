
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
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()

