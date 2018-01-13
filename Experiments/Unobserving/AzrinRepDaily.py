#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 13:33:55 2017

@author: benjaminlibman

Event Key:
100 - BO Left
110 - BO Right
120 - FR Left
130 - FR Right
200 - Pellet
300 - Start FR
400 - Start BO
410 - End BO

"""
from __future__ import division

#import os
#import platform
#import csv
#import glob

import numpy as np
import pandas as pd

#import matplotlib.pyplot as plt

ba1655 = '/Users/benjaminlibman/Google Drive/Academics/CMU/Lab/Research/Unobserving/Data/RF/BA1655.csv'


data = pd.read_csv(ba1655, sep=',', header=0, index_col=None)
data = data[data.runnum == 19]
data.head()

frr_irt_ = [round(i-j, 3) for i, j in zip(data.time[data.event == 120], data.time[data.event == 120].shift())]
frr_irt_[0] = 0

uor_irt_ = [round(i-j, 3) for i, j in zip(data.time[data.event == 110], data.time[data.event == 110].shift())]
if len(uor_irt_) == 0:
    uor_irt_ = [0]
else:
    uor_irt_[0] = 0
    
pellets = len(data[data.event == 200])+1

frr_irt = round(np.mean(frr_irt_), 3)
uor_irt = round(np.mean(uor_irt_), 3)
fr_resps = len(frr_irt_)
uo_resps = len(uor_irt_)-1
resps = fr_resps + uo_resps
r_SR = resps/pellets
frr_rate = round(resps/sum(frr_irt_), 3)

uo_num = len(data[data.event == 400])
fr_num = len(data[data.event == 300])

frpointer = []

count = 0
for i in data.event:
    if i == 120:
        count += 1
        frpointer.append(count)
    if i == 200:
        count = 0
        frpointer.append(count)

#print data[(data.event == 120)&(data.event == 200)]

for i, j in zip(frpointer, data.event):
    pass
    if j == 120 or j == 200:
        print i, j
        
        
print len(frpointer), len(frr_irt_)