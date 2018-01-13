'''
event key:
100 - BO Left
110 - BO Right
120 - FR Left
130 - FR Right
200 - Pellet
300 - Start FR
400 - Start BO
410 - End BO
'''
from __future__ import division

import numpy as np
import pandas as pd

MAINDIR = '/Users/benjaminlibman/Google Drive/Academics/CMU/Lab/Research/Unobserving/Data/'
RAW = MAINDIR + 'MedPC-Data/'
RF = MAINDIR + 'RF/Exp 4/'
RF2 = MAINDIR + 'RF2/'
SUMS = MAINDIR + 'Sums/Exp 4/'

def summary(inname, inpath, outpath):
    dset = pd.read_csv(inpath, sep=',', header=0, index_col=None)

    sumed = pd.DataFrame()

    date = []
    runnum = []
    fr = []
    pell25, pell100 = [], []
    fr_irt25, fr_irt100 = [], []
    resps25, resps100 = [], []
    uo_total25, uo_total100 = [], []
    fr_runrate25, fr_runrate100 = [], []
    prp25, prp100 = [], []
    sr_rate25, sr_rate100= [], []
    iri25,iri100 = [], []
    to_sr25, to_sr100 = [], []
    passnum = []    
    propBOfr100 = []
    propBOfr25 = []
    
    for run in set(dset.runnum):
        thisRun = run
        data = dset[dset.runnum == thisRun]#int('{}'.format(run))

        uor_irt_ = [round(i-j, 3) for i, j in zip(data.time[data.event == 110], data.time[data.event == 110].shift())]
        if len(uor_irt_) == 0:
            uor_irt_ = [0]
        else:
            uor_irt_[0] = 0

        uol_irt_ = [round(i-j, 3) for i, j in zip(data.time[data.event == 100], data.time[data.event == 100].shift())]
        if len(uol_irt_) == 0:
            uol_irt_ = [0]
        else:
            uol_irt_[0] = 0

        fr100_bo_time = []
        for i, j in zip(data.time, data.event):
            if j == 410 or j == 130 or j == 150 or j == 170:
                fr100_bo_time.append(i)
        
        fr25_bo_time = []
        for i, j in zip(data.time, data.event):
            if j == 400 or j == 120 or j == 140 or j == 160:
                fr25_bo_time.append(i)

        fr100_time = []
        for i, j in zip(data.time, data.event):
            if j == 410 or j == 130 or j == 150 or j == 170 or j == 310 or j == 110:
                fr100_time.append(i)
        
        fr25_time = []
        for i, j in zip(data.time, data.event):
            if j == 400 or j == 120 or j == 140 or j == 160 or j == 300 or j == 100:
                fr25_time.append(i)

        sr25 = len(data.event[data.event == 200])
        sr100 = len(data.event[data.event == 210])


        date.append(data.date.iloc[1])
        runnum.append(data.frval.iloc[1])
        pell25.append(sr25)
        pell100.append(sr100)

        fr_irt25.append(round(np.mean(data.fr_irt25[data.fr_irt25.notnull()]), 3))
        fr_irt100.append(round(np.mean(data.fr_irt100[data.fr_irt100.notnull()]), 3))
        uo_total25.append(len(data.event[data.event == 120]))
        uo_total100.append(len(data.event[data.event == 130]))
        resps25.append(len(data.frpointer25[data.frpointer25 > 0]))
        resps100.append(len(data.frpointer100[data.frpointer100 > 0]))
        fr_runrate25.append(round((len(data.fr_irt25[data.fr_irt25.notnull()])/sum(data.fr_irt25[data.fr_irt25.notnull()]))*60, 3))
        fr_runrate100.append(round((len(data.fr_irt100[data.fr_irt100.notnull()])/sum(data.fr_irt100[data.fr_irt100.notnull()]))*60, 3))
        prp25.append(round(np.mean(data.prp25[(data.prp25.notnull())]), 3))
        prp100.append(round(np.mean(data.prp100[(data.prp100.notnull())]), 3))
        sr_rate25 = [round(i/j, 3) for i, j in zip(pell25, fr_irt25)]
        sr_rate100 = [round(i/j, 3) for i, j in zip(pell100, fr_irt100)]
        iri25 = [round(1/i, 3) for i in sr_rate25]
        iri100 = [round(1/i, 3) for i in sr_rate100]        
        
        propBOfr25.append(round((sum(fr100_bo_time)/sum(fr100_time))*100, 3))
        propBOfr100.append(round((sum(fr25_bo_time)/sum(fr25_time))*100, 3))

    for i in runnum:
         passnum.append(0)

    thispass = 0
    for (i, j), (k, l) in zip(enumerate(runnum), enumerate(passnum)):
        if j == 1:
            thispass += 1
        passnum[k] = thispass

    sumed = sumed.assign(date = date)
    sumed = sumed.assign(passnum=passnum)
    sumed = sumed.assign(pell25=pell25)
    sumed = sumed.assign(pell100=pell100)
    sumed = sumed.assign(fr_irt25=fr_irt25)
    sumed = sumed.assign(fr_irt100=fr_irt100)
    sumed = sumed.assign(uo_total25=uo_total25)
    sumed = sumed.assign(uo_total100=uo_total100)
    sumed = sumed.assign(resps25=resps25)
    sumed = sumed.assign(resps100=resps100)
    sumed = sumed.assign(fr_runrate25=fr_runrate25)
    sumed = sumed.assign(fr_runrate100=fr_runrate100)
    sumed = sumed.assign(prp25=prp25)
    sumed = sumed.assign(prp100=prp100)
    sumed = sumed.assign(sr_rate25=sr_rate25)
    sumed = sumed.assign(sr_rate100=sr_rate100)
    sumed = sumed.assign(propBOfr100=propBOfr100)
    sumed = sumed.assign(propBOfr25=propBOfr25)

    sumed = sumed[['date', 'passnum', 'pell25','pell100', 'fr_irt25', 'fr_irt100', 'fr_runrate25', 'fr_runrate100', 'prp25', 'prp100', 'propBOfr100', 'propBOfr25', 'sr_rate25', 'sr_rate100', 'resps25', 'resps100', 'uo_total25', 'uo_total100']]
    
    sumed.to_csv(outpath, index=None, sep=',')

rats = ['BA1655', 'BA1656', 'BA1657', 'BA1658']

for rat in rats:
    summary(rat, RF + rat + '_C.csv' .format(rat), SUMS + rat + 'sums-E4.csv')