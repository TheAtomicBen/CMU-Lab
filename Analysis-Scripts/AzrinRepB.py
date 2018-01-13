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
RF = MAINDIR + 'RF/'
RF2 = MAINDIR + 'RF2/'
SUMS = MAINDIR + 'Sums/'

def summary(inname, inpath, outpath):
    dset = pd.read_csv(inpath, sep=',', header=0, index_col=None)
    dset = dset[dset.date != '11/12/17']
    dset = dset[dset.date != '11/18/17']
    
    if rat == 'BA1657':
        dset = dset[dset.date != '11/25/17']

    sumed = pd.DataFrame()

    date = []
    runnum = []
    fr = []
    pellets = []
    fr_irt = []
    uor_irt = []
    uol_irt = []
    uo_total = []
    fr_resps = []
    uo_resps = []
    resps = []
    r_SR = []
    fr_runrate = []
    fr_total_Rate = []
    prp = []
    fr_prp = []
    uo_prp = []
    sr_rate = []
    iri = []
    to_sr = []
    passnum = []


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

        sr = max(set(data.frpointer))

        date.append(data.date.iloc[1])
        runnum.append(data.ratio.iloc[1]/25)
        fr.append(data.ratio.iloc[1])
        pellets.append(len(data[data.frpointer == sr]))

        fr_irt.append(round(np.mean(data.fr_irt[data.frpointer > 1]), 3))
        uor_irt.append(round(np.mean(uor_irt_), 3))
        uol_irt.append(round(np.mean(uol_irt_), 3))
        fr_resps.append(len(data.fr_irt[data.frpointer > 0]))
        uo_resps.append(len(data.borpointer[data.borpointer > 0]) + len(data.bolpointer[data.bolpointer > 0]))
        uo_total.append(len(data.event[data.event == 400]))
        resps.append(len(data.event[data.event < 200]))
        r_SR.append(round((len(data.event[data.event < 200])/(len(data[data.frpointer == sr]))), 3))

        fr_runrate.append(round((len(data.event[data.event == 120])/sum(data.fr_irt[data.frpointer.shift() > 0]))*60, 3))
        fr_total_Rate.append(round((len(data.event[data.event == 120])/(sum(data.fr_irt[data.frpointer > 1])+sum(data.fr_prp[data.prp > 0])))*60, 3))

        prp.append(round(np.mean(data.prp[(data.prp > 0)&(data.time.shift() > 0)]), 3))
        fr_prp.append(round(np.mean(data.fr_prp[(data.fr_prp > 0)&(data.time.shift() > 0)]), 3))
        uo_prp.append(round(np.mean(data.uo_prp[(data.uo_prp > 0)&(data.time.shift() > 0)]), 3))

        sr_rate.append(round((len(data.event[data.event == 200])/sum(data.fr_irt[data.frpointer > 1]))*60, 3))
        iri.append(round(1/((len(data.event[data.event == 200])/sum(data.fr_irt[data.frpointer > 1]))), 3))

        to_sr.append(round((len(data.event[data.event == 400]))/(len(data.event[data.event == 400])+len(data[data.frpointer == sr])), 3))

    for i in runnum:
         passnum.append(0)

    thispass = 0
    for (i, j), (k, l) in zip(enumerate(runnum), enumerate(passnum)):
        if j == 1:
            thispass += 1
        passnum[k] = thispass

    sumed = sumed.assign(date = date)
    sumed = sumed.assign(passnum=passnum)
    sumed = sumed.assign(fr=fr)
    sumed = sumed.assign(pellets=pellets)
    sumed = sumed.assign(fr_irt=fr_irt)
    sumed = sumed.assign(uor_irt=uor_irt)
    sumed = sumed.assign(uol_irt=uol_irt)
    sumed = sumed.assign(uo_total=uo_total)
    sumed = sumed.assign(fr_resps=fr_resps)
    sumed = sumed.assign(uo_resps=uo_resps)
    sumed = sumed.assign(resps=resps)
    sumed = sumed.assign(r_SR=r_SR)
    sumed = sumed.assign(fr_runrate=fr_runrate)
    sumed = sumed.assign(fr_total_Rate=fr_total_Rate)
    sumed = sumed.assign(prp=prp)
    sumed = sumed.assign(fr_prp=fr_prp)
    sumed = sumed.assign(uo_prp=uo_prp)
    sumed = sumed.assign(sr_rate=sr_rate)
    sumed = sumed.assign(to_sr=to_sr)

    sumed = sumed[['passnum', 'fr', 'pellets', 'fr_irt', 'uor_irt', 'uol_irt', 'fr_resps', 'uo_resps', 'resps', 'r_SR', 'fr_runrate', 'uo_total', 'prp', 'fr_prp', 'uo_prp', 'fr_total_Rate', 'sr_rate', 'to_sr']]
    
    sumed.to_csv(outpath, index=None, sep=',')

rats = ['BA1655', 'BA1656', 'BA1657', 'BA1658']

for rat in rats:
    if 'BA1657' in rat:
        summary(rat, RF + rat + '.csv' .format(rat), SUMS + rat + 'sums-E2.csv')
    else:
        summary(rat, RF + rat + '.csv' .format(rat), SUMS + rat + 'sums-E3.csv')
    
