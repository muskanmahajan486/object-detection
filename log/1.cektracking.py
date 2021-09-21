import cv2
import numpy as np

def hough(orig_frame):
    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low_yellow = np.array([0, 0, 215])
    up_yellow = np.array([117, 255, 255])
    mask = cv2.inRange(hsv, low_yellow, up_yellow)
    edges = cv2.Canny(mask, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    kluar = frame
    return kluar



def nothing(x):
    pass
cv2.namedWindow('Trackbar')

cap = cv2.VideoCapture("danu1.mp4")
#cap = cv2.VideoCapture(0)
#cap.set(3,320);
#cap.set(4,240);

H_bawah = 20
H_atas = 48

S_bawah = 110
S_atas = 176

V_bawah = 130
V_atas = 255



ukuran = 0

cv2.createTrackbar('H_bawah','Trackbar',H_bawah,255,nothing)
cv2.createTrackbar('H_atas','Trackbar',H_atas,255,nothing)

cv2.createTrackbar('S_bawah','Trackbar',S_bawah,255,nothing)
cv2.createTrackbar('S_atas','Trackbar',S_atas,255,nothing)

cv2.createTrackbar('V_bawah','Trackbar',V_bawah,255,nothing)
cv2.createTrackbar('V_atas','Trackbar',V_atas,255,nothing)

cv2.createTrackbar('ukuran','Trackbar',ukuran,255,nothing)

fou = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('fra.avi', fou, 60.0, (320, 240))

def my_mouse_callback(event,x,y,flags,param):
    global hsv
    if event == cv2.EVENT_LBUTTONUP:
        print("warna:")
        print(hsv[y,x])
        cv2.setTrackbarPos('H_bawah', 'Trackbar', hsv[y,x][0]-25)
        cv2.setTrackbarPos('H_atas', 'Trackbar', hsv[y,x][0]+25)
        cv2.setTrackbarPos('S_bawah', 'Trackbar', hsv[y,x][1])
        cv2.setTrackbarPos('V_bawah', 'Trackbar', hsv[y,x][2])
    if event == cv2.EVENT_RBUTTONUP:
        print("x,y", x, y)
        cv2.waitKey(2000)

cv2.namedWindow("frame")
cv2.setMouseCallback("frame",my_mouse_callback)

tr2 = 0
daa = []
while(1):
    
    ret,frame = cap.read()
    #cv2.rectangle(frame, (1086, 66), (1244, 114), (0, 0, 0), -1)
    ret,frame2 = cap.read()
    ret,frame3 = cap.read()
    # frame3 = hough(frame)
    
   # frame = cv2.imread('im2.jpeg',1)#cap.read()
  #  frame2 = cv2.imread('im2.jpeg',1)#cap.read()
  #  frame3 = cv2.imread('im2.jpeg',1)#cap.read()
    #frame = frame[400:100, 0:700]
   # frame2 = frame2[400:10, 0:700]
   # frame3 = frame3[400:0, 0:700]
    
    try :
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    except cv2.error:
        break
    H_bawah = cv2.getTrackbarPos('H_bawah','Trackbar')
    S_bawah = cv2.getTrackbarPos('S_bawah','Trackbar')
    V_bawah = cv2.getTrackbarPos('V_bawah','Trackbar')
    
    H_atas = cv2.getTrackbarPos('H_atas','Trackbar')
    S_atas = cv2.getTrackbarPos('S_atas','Trackbar')
    V_atas = cv2.getTrackbarPos('V_atas','Trackbar')

    ukuran = cv2.getTrackbarPos('ukuran','Trackbar')

    batas_atas = np.array([H_atas,S_atas,V_atas])
    batas_bawah = np.array([H_bawah,S_bawah,V_bawah])
    
    mask = cv2.inRange(hsv, batas_bawah, batas_atas)
    kernel = np.ones((10,10), np.uint8)
    hasil_dilasi = cv2.erode(mask, kernel)
    kernel2 = np.ones((10,10), np.uint8)
    hasil_erosi = cv2.erode(hasil_dilasi, kernel2)
    x, y, w, h = cv2.boundingRect(hasil_erosi)
    #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
    print(x,y)
    if w*h>ukuran and (w*h<1000000):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (10, 255, 0), 5)
        #res = cv2.bitwise_and(frame2,frame2, mask= hasil_dilasi)
        daa.append((x+int(w/2), y+int(h/2) ))
    print("panjang array : ", len(daa))
    
    #cv2.line(frame,daa[0],daa[len(daa)-1],(0,255,0),2)#ini
    '''
    #hs = daa[len(daa)-1][0] - daa[0][0] #nilai x
    #hs2 = daa[len(daa)-1][1] - daa[0][1] #milai y
    #if hs<0: hs = hs*-1
    if hs2<0: hs2 = hs2*-1
    hs = int(hs/1.8)
    hs2 = int(hs2/1.8)
    print(hs, hs2)
    '''
    
    
    
    for ko in range(1,len(daa)):
        #if ko < 456:
        #print(ko)
        cv2.circle(frame,daa[ko], 5, (0,255,0), -1)
        cv2.line(frame,daa[ko],daa[ko-1],(0,0,255),2)
        
    #garis
    #gray = cv2.cvtColor(frame3,cv2.COLOR_BGR2GRAY)
    #edges = cv2.Canny(gray,50,150,apertureSize = 3)
    #cv2.imshow('edges',edges)

   # lines = cv2.HoughLinesP(edges,1,np.pi/180,100)
   # for x1,y1,x2,y2 in lines[0]:
     #   cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
     

    #cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)
        
    
    
    hasil_erosi = cv2.resize(hasil_erosi, (940,640))
    cv2.imshow('mask',hasil_erosi)
    #cv2.imshow('res',res)
    try :
        #frame3 = cv2.resize(frame, (100,100))
        #cv2.imshow('frame3',frame3)
        out.write(frame)
    except cv2.error:
        break
    

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    frame = cv2.resize(frame, (940,640))
    cv2.imshow('frame',frame)
    cv2.imwrite("da.jpg", frame)


cap.release()
out.release()
cv2.destroyAllWindows()
