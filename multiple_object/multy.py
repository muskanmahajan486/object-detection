import cv2
import numpy as np
import sys
import time
import RPi.GPIO as GPIO

StepPinForward=36
StepPinBackward=37
buzzer = 10
servoPIN = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(StepPinForward, GPIO.OUT)
GPIO.setup(StepPinBackward, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT) 

global Buzz 
Buzz = GPIO.PWM(buzzer, 440) 
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization

def forward(x):
	GPIO.output(StepPinForward, GPIO.HIGH)
	print "forwarding running motor"
	time.sleep(x)
	GPIO.output(StepPinForward, GPIO.LOW)

def reverse(x):
	GPIO.output(StepPinBackward, GPIO.HIGH)
	print "backwarding running motor"
	time.sleep(x)
	GPIO.output(StepPinBackward, GPIO.LOW)

def stop(x):
	GPIO.output(StepPinBackward, GPIO.LOW)
	print "stop motor"
	time.sleep(x)
	GPIO.output(StepPinBackward, GPIO.LOW)


def callback(x):
	pass
    
############## kuning################

ilowH_1 = 0
ihighH_1 = 72
ilowS_1 = 70
ihighS_1 = 247
ilowV_1 = 140
ihighV_1 =255

############## Biru ################
ilowH_2 = 50
ihighH_2 = 70
ilowS_2 = 50
ihighS_2 = 255
ilowV_2 = 120
ihighV_2 =255

frame_w = 440
frame_h = 85


min_obj = 10*20
max_obj = frame_w*frame_h/1

count = 0


kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))


def contour(mask,color):
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    (_,conts,_)=cv2.findContours(maskFinal.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        
    for countour in conts:
        objectFound = 0
        area = cv2.contourArea(countour)
        

        if ((area <max_obj) & (area >min_obj)):			
            objectFound = 1
            
            
            cv2.drawContours(frame,conts,-1,(255,0,0),3)
        
            for i in range(len(conts)):
                x,y,w,h=cv2.boundingRect(conts[i])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0), 2)
                # cv2.putText(frame,str(area),(x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,0,255), 2)
                # if (count>=2):

                cv2.putText(frame,'Object Found',(50,50), cv2.FONT_HERSHEY_COMPLEX, 2 ,(0,255,0), 2)
                cv2.putText(frame,color,(x, y - 50), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,255,0), 2)
        
        else:
            for i in range(len(conts)):
                x,y,w,h=cv2.boundingRect(conts[i])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)


        if (objectFound==True):
			Buzz.start(50) 
			Buzz.ChangeFrequency(500)
			print("on")
			#forward(2)
			p.ChangeDutyCycle(5)
			
			#GPIO.output(buzzer,False)
			print("off")
			#stop(1)
			objectFound = 0
			count = 0
		else:
			Buzz.start(0)
			p.ChangeDutyCycle(12)
           

cap = cv2.VideoCapture(0)
while(1):

    # Take each frame
    ret, frame=cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_1 = np.array([ilowH_1, ilowS_1, ilowV_1])
    upper_1 = np.array([ihighH_1, ihighS_1, ihighV_1])

    lower_2 = np.array([ilowH_2, ilowS_2, ilowV_2])
    upper_2 = np.array([ihighH_2, ihighS_2, ihighV_2])

    mask_2 = cv2.inRange(hsv, lower_2, upper_2) # I have the Green threshold image.

    # Threshold the HSV image to get only blue colors
    mask_1 = cv2.inRange(hsv, lower_1, upper_1)
    mask = mask_1 + mask_2

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    contour(mask_1,"KUNING")
    contour(mask_2,"BIRU")

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    # cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()