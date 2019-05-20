import cv2
import numpy as np

cam = cv2.VideoCapture(0)
_, frame = cam.read();
#img = cv2.imread("frame.jpg")
cv2.imshow("img original", frame)
imgHSV = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2HSV) 
(h, s, v) = cv2.split(imgHSV)
h= h+20
h = np.clip(h, 0, 255)
#s = s*2
#s = np.clip(s, 0, 255)
imgHSV = cv2.merge([h, s, v])

imgBGR = cv2.cvtColor(imgHSV, cv2.COLOR_HSV2BGR)
#cv2.imwrite("saturated.jpg", imgBGR)
cv2.imshow("img saturated", imgBGR)
cv2.waitKey(0)
