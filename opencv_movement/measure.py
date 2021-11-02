import cv2 as cv
import numpy as np
import math

ilowH = 20
ilowS = 110
ilowV = 130
ihighH = 48
ihighS = 176
ihighV = 255

# ilowH = 20
# ilowS = 220
# ilowV = 154
# ihighH = 255
# ihighS = 255
# ihighV = 255

WIDTH = 800
HEIGHT = 700

cap = cv.VideoCapture('log/l3.mp4')
cv.namedWindow('image',cv.WINDOW_NORMAL)
import matplotlib.pyplot as plt


list_trig_x=[]
list_trig_y=[]
length =0
max_length = 0

x_prev = 0
y_prev = 0
point_w_start = 0
point_w_end = 0
point_h_start = 0
point_h_end = 0
length_w = 0
length_h = 0
count_point = 0
switch_track = False
calibration_factor = 0.212857143 
container_y = 0
container_y2 = 0
container_x = 0
center_y_prevs = 0
center_x_prevs = 0
y_points = 0



def callback(x):
    pass

data_point = {
    'x':[],
    'y':[]
}

def add_data(x,y):
    data_point['x'].append(x)
    data_point['y'].append(y)

def draw_ball_location(img_color, locations):
    for i in range(len(locations)-1):

        if locations[0] is None or locations[1] is None:
            continue
        


        loc1 = (30,200)
        loc2 = (70,90)
        cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (0, 255, 255), 2)

        # add_data( [locations[i][0],locations[i+1][0]], [HEIGHT- locations[i][1],HEIGHT-locations[i+1][1]] )
        # add_data( locations[i][0], locations[i][1] )

        # -------try realtime------
        # cv.line(img_color,loc1 , loc2 ,(0, 255, 255), 3)
        # plt.plot(locations[i], locations[i+1], 'ro')
        # print(locations[i][0])
        # print(locations[i][1])
        # print("-")
        # print(locations[i+1])
        # print("p")
        
        # x1, y1 = [locations[i][0],locations[i+1][0]], [locations[i][1],locations[i+1][1]]
        


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
    try:
        ret,img_color = cap.read()
        
        # ---scale---
        # scale_percent = 50 # percent of original size
        # width = int(img_color.shape[1] * scale_percent / 100)
        # height = int(img_color.shape[0] * scale_percent / 100)
        
        # ---manual---
        width =WIDTH
        height = HEIGHT
        dim = (width, height)
        
        
        # resize image
        img_color = cv.resize(img_color, dim, interpolation = cv.INTER_AREA)

        # rotate
        center = (width/2, height/2) 
        # using cv2.getRotationMatrix2D() to get the rotation matrix

        rotate_matrix = cv.getRotationMatrix2D(center=center, angle=90, scale=1)
        # rotate the image using cv2.warpAffine
        img_color = cv.warpAffine(src=img_color, M=rotate_matrix, dsize=(width, height))
        

        # img_color = cv.flip(img_color, 1) # flip


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


            cv.rectangle(img_color, (left, top), (left + width, top + height), (255, 0,0 ), 5)
            # cv.circle(img_color, (center_x, center_y), 10, (0, 255, 0), -1)

            if isDraw:
                list_ball_location.append((center_x, center_y))
                add_data(center_x,HEIGHT-center_y) # make plot
                # print("---------")
            
            # else:
                # history_ball_locations.append(list_ball_location.copy())
                # list_ball_location.clear()

        img_color = draw_ball_location(img_color, list_ball_location)

        



        if list_ball_location :
            if(switch_track == False):
                count_point +=1
                if(count_point ==1):
                    point_w_start = center_x
                    point_h_start = center_y

                point_w_end = center_x
                point_h_end = center_y
                # length_w = point_w_end - point_w_start

                length_w = int(np.sqrt((point_w_end - point_w_start)**2 + (point_h_start - point_h_end)**2))

                #  length_real / length_pixel
                #  teshold = 0.092857143

                length_real = length_w * calibration_factor 
                
                #===============================================================================
                print("----------",center_x)
                if(list_trig_x):

                    if(center_y <= list_trig_y[-1] ):
                        container_y += abs(center_y_prevs - center_y)
                      
                    if(center_y >= list_trig_y[-1] ):
                        container_y2 += abs(center_y_prevs - center_y)
                      
                    if(center_x <= list_trig_x[-1]):
                        container_x += abs(center_x_prevs - center_x)
                        length +=1
                    else:
                        length = 0
                        container_x = 0
                        container_y = 0
                        container_y2 = 0

                    center_y_prevs = center_y
                    center_x_prevs = center_x

                    print("x ------",container_x,"|||| y-----------",container_y,"y2-----------",container_y2)

                if(length > max_length and center_x > 100):
                   
                    if(container_y > container_y2):
                        y_points = container_y
                    else:
                        y_points = container_y2

                    pythagoras = np.sqrt(container_x**2 +y_points**2)
                    rad = math.sin(y_points/pythagoras)
                    degress = math.degrees(rad)

                    print("deg >",degress)

                    # if(container_x > container_y+50 or container_x > container_y2+40):
                    
                    if(degress < 15):
                        max_length = length #11

                print("max==================",max_length)
                x_prev = center_x
                y_prev = center_y
                
                if(max_length >= 11):
                    switch_track = True
                    point_w_start = center_x+50
                    point_h_start = center_y
                    x_prev = point_w_start

                list_trig_x.append(center_x)
                list_trig_y.append(center_y)
                # cv.putText(img_color,str(length_real),(center_x, center_y - 20), cv.FONT_HERSHEY_COMPLEX, 1 ,(0,0,255), 2)
            else:
                point_w_end = center_x
                point_h_end = center_y
                # length_w = point_w_end - point_w_start

                length_w = int(np.sqrt((point_w_end - point_w_start)**2 + (point_h_start - point_h_end)**2))

                #  length_real / length_pixel
                #  teshold = 0.092857143

                length_real_switch = length_w * calibration_factor 
            
                print("----------",length_real)
                cv.putText(img_color,str("{:.2f} cm".format(length_real_switch)),(center_x - 60, point_h_start + int((center_y-point_h_start)/2)), cv.FONT_HERSHEY_COMPLEX, 1 ,(0,0,0), 2)
                cv.line(img_color, (point_w_start,point_h_start), tuple(list_ball_location[-1]), (0, 50, 255), 3)
            
            cv.putText(img_color,str("{:.2f} cm".format(length_real)),(list_ball_location[0][0] + int((x_prev - list_ball_location[0][0])/2), y_prev - 40), cv.FONT_HERSHEY_COMPLEX, 1 ,(0,0,0), 2)
            cv.line(img_color, tuple(list_ball_location[0]), (x_prev,y_prev), (0, 0, 255), 3)
          
        
        # for ball_locations in history_ball_locations:
        #     img_color = draw_ball_location(img_color, ball_locations)

        # print(length)
        
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
    except:
        print("show plot")   
        # print(data_point['x'])    
        print(list_ball_location)   
        plt.plot(data_point['x'],data_point['y'], 'r')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.ylim([100, 700])
        plt.show()
        break
