import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

ilowH = 20
ilowS = 88
ilowV = 76
ihighH = 48
ihighS = 95
ihighV = 255


cap = cv.VideoCapture(0)
cv.namedWindow('image',cv.WINDOW_NORMAL)

def callback(x):
    pass

def draw_ball_location(img_color, locations):
    for i in range(len(locations)-1):

        if locations[0] is None or locations[1] is None:
            continue
        
        loc1 = (30,200)
        loc2 = (70,90)
        cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (0, 255, 255), 3)
        # cv.line(img_color,loc1 , loc2 ,(0, 255, 255), 3)
        # plt.plot(locations[i], locations[i+1], 'ro')
        # print(locations[i][0])
        # print(locations[i][1])
        # print("-")
        # print(locations[i+1])
        # print("p")
        x1, y1 = [locations[i][0],locations[i+1][0]], [locations[i][1],locations[i+1][1]]
        # x1, y1 = [loc1[0],loc2[0]], [loc1[1],loc2[1]]
        # plt.plot(x1, y1, marker = 'o')
        # plt.xlim([0, 600])
        # plt.ylim([0, 600])

        # # plt.axis([0, 6, 0, 20])
        # # y = np.random.random()
        # plt.pause(0.000001)
   
    return img_color

# create trackbars for color change
cv.createTrackbar('lowH','image',ilowH,255,callback)
cv.createTrackbar('lowS','image',ilowS,255,callback)
cv.createTrackbar('lowV','image',ilowV,255,callback)
cv.createTrackbar('highH','image',ihighH,255,callback)
cv.createTrackbar('highS','image',ihighS,255,callback)
cv.createTrackbar('highV','image',ihighV,255,callback)


list_ball_location = []
history_ball_locations = []
isDraw = True

while True:

    ret,img_color = cap.read()

    img_color = cv.flip(img_color, 1)


    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    ilowH = cv.getTrackbarPos('lowH', 'image')
    ilowS = cv.getTrackbarPos('lowS', 'image')
    ilowV = cv.getTrackbarPos('lowV', 'image')
    ihighH = cv.getTrackbarPos('highH', 'image')
    ihighS = cv.getTrackbarPos('highS', 'image')
    ihighV = cv.getTrackbarPos('highV', 'image')


    lower_hsv = np.array([ilowH, ilowS, ilowV])
    higher_hsv = np.array([ihighH, ihighS, ihighV])

    img_mask = cv.inRange(img_hsv, lower_hsv, higher_hsv)

    kernel = cv.getStructuringElement( cv.MORPH_RECT, ( 5, 5 ) )
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations = 3)

    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img_mask)

    max = -1
    max_index = -1 

    for i in range(nlabels):
 
        if i < 1:
            continue

        area = stats[i, cv.CC_STAT_AREA]

        if area > max:
            max = area
            max_index = i


    if max_index != -1:

        center_x = int(centroids[max_index, 0])
        center_y = int(centroids[max_index, 1]) 
        left = stats[max_index, cv.CC_STAT_LEFT]
        top = stats[max_index, cv.CC_STAT_TOP]
        width = stats[max_index, cv.CC_STAT_WIDTH]
        height = stats[max_index, cv.CC_STAT_HEIGHT]


        cv.rectangle(img_color, (left, top), (left + width, top + height), (0, 0, 255), 5)
        # cv.circle(img_color, (center_x, center_y), 10, (0, 255, 0), -1)

        if isDraw:
            list_ball_location.append((center_x, center_y))
            print("---------")
        
        else:
            history_ball_locations.append(list_ball_location.copy())
            list_ball_location.clear()


    img_color = draw_ball_location(img_color, list_ball_location)

    for ball_locations in history_ball_locations:
        img_color = draw_ball_location(img_color, ball_locations)

   
    cv.imshow('Blue', img_mask)
    cv.imshow('Result', img_color)
    
    key = cv.waitKey(1)
    if key == 27: # esc
        break
    elif key == 32: # space bar
        list_ball_location.clear()
        history_ball_locations.clear()
    elif key == ord('v'):
        isDraw = not isDraw
plt.show()