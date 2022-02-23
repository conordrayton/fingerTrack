import cv2
import mediapipe as mp
import time
import serial
import HandTrackingModule2 as htm
import sys
import numpy as np

#import module as htm then call detector=htm.detector()
arduino=serial.Serial("/dev/cu.usbmodem143301",9600)
print(arduino.name)


pTime = 0  # previous time
cTime = 0  # current time
# used to track the FP
cap = cv2.VideoCapture(0)
detector =htm.handDetector()  # default parameters already set

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    # find position method returns a list of hand positions
    if len(lmList) != 0:
        arr=lmList[8]
        print(arr)
        xxx=list(arr[1])  #how to access columns or no
        yyy=list(arr[2])
        xx=str(xxx)
        yy=str(yyy)
        data=[xx,yy]

        arduino.write(bytes(data,'utf-8'))
        # where land mark 4 is the tip of the thumb
        #arduino.write(lmList)


    # for calculating fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime  # previoustime becomes current time
    img = detector.findHands(img)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                (255, 0, 255), 3)
    # prints text on the image instead of the console
    # need to convert fps to a string and also round it
    # the rest is just the font, scale colour and thickness
    cv2.imshow("Image", img)
    cv2.waitKey(1)



