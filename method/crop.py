import cv2
import numpy as np

img = cv2.imread('papagaio.png')
output = img.copy()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,4,10000,param1=100,param2=4,minRadius=4,maxRadius=70)

if circles is not None:
    circles = np.round(circles[0,:]).astype("int")
    if len(circles) == 1:
        x,y,r = circles[0] 
        mask = np.zeros((img.shape[1],img.shape[0],3),np.uint8)
        cv2.circle(mask,(x,y),r,(255,255,255),-1,8,0)
        out = img*mask
        white = 255-mask
        cv2.imwrite('crop_mask1.png',out+white)
        cv2.imwrite('crop_mask2.png',out)
        cv2.imshow('cing', out)

cv2.waitKey(0)
cv2.destroyAllWindows()