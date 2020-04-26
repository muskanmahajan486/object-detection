import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
frame_w = 440
frame_h = 280
min_obj = 10*300
max_obj = frame_w*frame_h/1.5

while True:
      
        # im = cv.imread('test.jpg')
        ret, frame = cap.read()
        imgray = cv.cvtColor( frame, cv.COLOR_BGR2GRAY)
        
        ret, thresh = cv.threshold(imgray, 120, 250,cv.THRESH_BINARY_INV)
        # ret, otsu = cv.threshold(imgray, 0, 255, cv.THRESH_OTSU)
        
        
        # gray = cv2.bilateralFilter(gray, 11, 17, 17)
        #can= cv.Canny(imgray, 30, 200)

        conts,h= cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for countour in conts:
                area = cv.contourArea(countour)
                print ("area",area)

        
        #cv.drawContours(frame,conts,-1,(255,0,0),3)
        if ((area <20) & (area >0)):         
                cv.drawContours(frame,conts,-1,(0,255,0),3)
                print("done")
        

        cv.drawContours(frame,conts,-1,(0,0,255),3)
        cv.imshow("cam",frame)
        cv.imshow("tresh",thresh )
        if(cv.waitKey(1) & 0xFF == ord('q')):
                break
     
cap.release()
cv.destroyAllWindows()
