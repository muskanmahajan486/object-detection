from helper import *
import cv2
import numpy as np
import os
import pickle

# https://klassenresearch.orbs.com/Plotting+with+Python
from matplotlib import rc
# Make use of TeX﻿
rc('text',usetex=True)
# Change all fonts to 'Computer Modern'
rc('font',**{'family':'serif','serif':['Computer Modern']})

fileName = "yawLog5"

capture = cv2.VideoCapture(0)
dataLog = pickle.load( open( "cbjd.p", "rb" ) )
#dataLog.append(['pos'])
#dataLog['pos'] = []
#dataLog['pos'].append((1,2))
print(dataLog)
