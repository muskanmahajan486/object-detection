#!/usr/bin/python
# encoding: utf-8

from helper import *
import cv2
import numpy as np
import os
import pickle

# https://klassenresearch.orbs.com/Plotting+with+Python
#import matplotlib.rc

# Make use of TeX﻿
#rc('text',usetex=True)
# Change all fonts to 'Computer Modern'
#rc('font',**{'family':'serif','serif':['Computer Modern']})
fileName = "1"

cap = cv2.VideoCapture("danu1.mp4")

# dataLog = pickle.load( open( "cb.p", "rb" ) )
# dataLog2 = pickle.load( open( "cb.p", "rb" ) )
dataLog = {
    'videoTimestamp' : '',
    'pos' : ''
}

def nothing(x):
    pass
cv2.namedWindow('Trackbar')

#cap.set(3,320);
#cap.set(4,240);
# ilowH = 20
# ilowS = 110
# ilowV = 130
# ihighH = 48
# ihighS = 176
# ihighV = 255

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
        cv2.waitKey(2000)

cv2.namedWindow("frame")
cv2.setMouseCallback("frame",my_mouse_callback)

tr2 = 0


dataLog['videoTimestamp'] = []
dataLog['pos'] = []

first = True
while True:
    elapsedTime = cap.get(cv2.CAP_PROP_POS_MSEC)/1000.
    _, frame = cap.read()
    _, frame2 = cap.read()
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
    #print(x,y)
    if w*h>ukuran:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
    try :
        res = cv2.bitwise_and(frame2,frame2, mask= hasil_dilasi)
    except cv2.error:
        break
    frame = cv2.resize(frame, (940,640))
    cv2.imshow('frame',frame)
    mask = cv2.resize(mask, (940,640))
    cv2.imshow('mask',mask)
    res = cv2.resize(res, (940,640))
    cv2.imshow('res',res)
    dataLog['videoTimestamp'].append(elapsedTime)
    titik_lantai = 1308
    skala_jarak = 7 #hasil hitung dari jarak asli terukur/jarak pixel terukur
    hh = (y)/skala_jarak
    hh = int(hh)
    hi = (x)/skala_jarak
    hi= int(hi)
    dataLog['pos'].append(( hi, hh ))
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()  
pickle.dump( dataLog, open( "cbjd.p", "wb" ) )
#pickle.dump( dataLog2, open( "jadi2.p", "wb" ) )

