import numpy as np
import cv2
cap = cv2.VideoCapture(0)

kernelOpen=np.ones((10,10))
kernelClose=np.ones((20,20))

while True:

     # im = cv2.imread('test.jpg')
     ret, frame = cap.read()
     HSV = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV)
     irange = cv2.inRange(HSV ,(0, 59, 0), (179,194,130))
     # ret, thresh = cv2.threshold(imgray, 127, 250,cv2.THRESH_BINARY_INV)

     # # gray = cv22.bilateralFilter(gray, 11, 17, 17)
     can= cv2.Canny(HSV, 30, 200)

     maskOpen=cv2.morphologyEx(irange,cv2.MORPH_OPEN,kernelOpen)
     maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

     maskFinal=maskClose
     conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
     # cv2.drawContours(frame,img,-1,(255,0,0),3)
     for countour in conts:
          area = cv2.contourArea(countour)
          print ("area",area)

        
        #cv2.drawContours(frame,conts,-1,(255,0,0),3)
     if ((area <20) & (area >0)):         
          cv2.drawContours(frame,conts,-1,(0,255,0),3)
          print("done")
     else:
           cv2.drawContours(frame,conts,-1,(0,0,255),3)
     cv2.imshow("cam",frame)
     cv2.imshow("tresh",irange)
     cv2.imshow("can",can)

    
     if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

     
cap.release()
cv2.destroyAllWindows()
