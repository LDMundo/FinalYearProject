#import modules
import cv2
import numpy as np

#Capture video through default camera
cap = cv2.VideoCapture(0)
while True:_, img = cap.read()

#Convert img frame from BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
