import cv2

cap = cv2.VideoCapture("GOPR1149.avi")
fou = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('keluaran333.avi', fou, 20.0, (320, 240))
tr = 0

def my_mouse_callback(event,x,y,flags,param):
    global frame_hsv
    if event == cv2.EVENT_LBUTTONUP:
        print("Color:")
        print(frame_hsv[y,x])

cv2.namedWindow("image")
cv2.setMouseCallback("image",my_mouse_callback)

while(True):
    if cv2.waitKey(1) & 0xFF == ord('k'):
            tr = 1
            print("mulai")
    ret, fr = cap.read()
    if tr == 1:
        out.write(fr)
    try :
        cv2.imshow('image',fr)
    except cv2.error:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    frame_hsv = cv2.cvtColor(fr,cv2.COLOR_BGR2HSV)
cap.release()
out.release()
cv2.destroyAllWindows()
