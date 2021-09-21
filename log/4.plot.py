#!/usr/bin/python
# encoding: utf-8

#from helper import *

from pylab import *

import numpy as np
import pickle

# https://klassenresearch.orbs.com/Plotting+with+Python
from matplotlib import rc
# Make use of TeX﻿
#rc('text',usetex=True)
# Change all fonts to 'Computer Modern'
#rc('font',**{'family':'serif','serif':['Computer Modern']})


data_file_name = "lagi1"
data = pickle.load( open( "cbjd.p", "rb" ) )

ts = data['videoTimestamp']
pos = np.array(data['pos'])
#for sd in pos:
#    print(sd/6.04)
print(pos)

figure()
for dl in range(1,len(pos)):
    text(pos[dl][0]-10, (pos[dl][1])*-1,"o")
    text(pos[dl][0]-10, (pos[dl][1])*-1,str( pos[dl][1]) )
plot(pos[:,0], (pos[:,1]))
title('CATU DAYA BATERAI 12,3 VOLT', fontsize=16)
xlabel('Posisi X (Cm)', fontsize=16)
ylabel('Posisi Y (Cm)', fontsize=16)
axis('equal')
#tight_layout()
grid(True)
savefig("position_log.png")


'''
figure()
plot(ts, pos[:,0],'b')
plot(ts, pos[:,1],'g')
legend(["X","Y"])
xlabel('Time [seconds]', fontsize=16)
ylabel('Position [cm]', fontsize=16)
tight_layout()
grid(True)
savefig("position_vs_time.png")
'''
show()

