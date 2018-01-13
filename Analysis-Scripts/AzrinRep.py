'''

medPc-RF.py
This file is designed to import a Med-PC text file and reformat it into columns and rows.
KEY (pre 092117)
100: 'left'
110: 'right' 
300: 'iti'
310: 'fr5'

KEY:
100 - BO Left
110 - BO Right
120 - FR Left
130 - FR Right
200 - Pellet
300 - Start FR
400 - Start BO
410 - End BO       
'''

#=============================================Imports==============================================
from __future__ import division

import os
# import platform
import csv
import glob

from itertools import izip

import numpy as np
import pandas as pd

#============================================Main Var Defs=========================================
MAINDIR = '/Users/benjaminlibman/Google Drive/Academics/CMU/Lab/Research/Unobserving/Data/'
RAW = MAINDIR + 'MedPC-Data/' + 'Exp3/'
RF = MAINDIR + 'RF/'
RF2 = MAINDIR + 'RF2/'
SUMS = 'Sums/'

HEADER = ['DATE', 'SUBJECT', 'INDEX', 'TIME_CODE']

files = []
rats = []
rundates = []
#=============================================Start Code===========================================
#==========================================Convert to .CSV=========================================
# for f in glob.glob(RAW + '*.Group_1'):
#     files.append(f)
#     rats.append(str(f[-40:-34]))


def wrangler(inname, inpath, outpath):
    if os.path.exists(outpath):
        os.remove(outpath)
    else:
        pass

    ba50 = pd.read_table(inpath, skiprows=[0], header=None, index_col=False)

    date = []
    subject = []
    a_array = []
    c_array = []

    arrayType = []
    datecol = []
    runnum_a = []
    runnum_c = []

    expType = []
    FR = []
    pellets = []

    subj = []
    ratio = []

    for i in ba50[0]:
        if 'Start Date:' in i:
            date.append(i[12:])
        if 'Subject' in i:
            subject.append(i[9:])
        if 'A:' in i:
            a_array.append(i[0])
        if 'C:' in i:
            c_array.append(i[0])

    ba50 = ba50[(ba50[0].str.contains('Start Date:') == False)&
                (ba50[0].str.contains('End Date:') == False)&
                (ba50[0].str.contains('Subject:') == False)&
                (ba50[0].str.contains('Experiment:') == False)&
                (ba50[0].str.contains('Group:') == False)&
                (ba50[0].str.contains('Box:') == False)&
                (ba50[0].str.contains('Start Time:') == False)&
                (ba50[0].str.contains('End Time:') == False)&
                (ba50[0].str.contains('MSN:') == False)]

    for i in ba50[0]:
        if '-' in i or 'A' in i or '0.000' in i:
            arrayType.append(1)
        elif '-' not in i or 'C' in i:
            arrayType.append(2)

    # arrayType = pd.Series(arrayType)
    ba50['arrayType'] = arrayType

    ba50_a = ba50[ba50.arrayType == 1]
    ba50_c = ba50[ba50.arrayType == 2]

    count_a = 0

    for i in ba50_a[0]:
        if 'A' in i:
            count_a +=1
        runnum_a.append(count_a)

    count_c = 0
    for i in ba50_c[0]:
        if 'C' in i:
            count_c +=1
        runnum_c.append(count_c)

    # ba50_a = ba50_a.assign(runnum=runnum_a) #<--------- Set the new runnum array without warnings
    ba50_c = ba50_c.assign(runnum=runnum_c)   #<--------- Set the new runnum array without warnings

    ba50_a = ba50_a[ba50[0].str.contains('A:') == False]

    for i in ba50_a[0]:
        if '0:' in i:
            expType_ = i.strip()[9:].split('.')
            expType.append(int(expType_[0])*-1)
        if '1:' in i:
            fr = i.strip()[8:].split('.')
            FR.append(abs(int(fr[0])))
        if '3:' in i:
            pellets_ = i.strip()[9:].split('.')
            pellets.append(int(pellets_[0]))

    for i in runnum_c:
        datecol.append(date[0])
        subj.append(subject[0])
        ratio.append(FR[0])

    idx = -1
    for i, (j, k) in izip(ba50_c.runnum.shift(), enumerate(ba50_c.runnum)):
        if i == k:
            datecol[j] = date[idx]
            ratio[j] = FR[idx]
        if i != k:
            idx += 1

    ba50_c = ba50_c.assign(date=datecol) #<--------- Set the new date array without warnings
    ba50_c = ba50_c.assign(subject=subj) #<--------- Set the new subject name array without warnings
    ba50_c = ba50_c.assign(ratio=ratio)  #<--------- Set the new date array without warnings

    ba50_c = ba50_c[ba50_c[0].str.contains('C:') == False]
    time_code = []
    time = []
    code = []


    for i in ba50_c[0]:
        time_code.append(i.strip().split(':')[1].strip())

    for i in time_code:
        time.append(int(i.strip().split('.')[0])/100)
        code.append(int(i.strip().split('.')[1]))

    ba50_c = ba50_c.assign(time=time)  #<--------- Set the new time array without warnings
    ba50_c = ba50_c.assign(event=code) #<--------- Set the new code array without warnings

    frpointer = []
    frpointerB = []
    borpointer = []
    bolpointer = []

    fr_irt = []
    fr_prp = []
    uo_prp = []
    prp = []

    trial = []
    trial2 = []

    #initialize pointers
    for i in ba50_c.event:
        frpointer.append(0)
        frpointerB.append(0)
        borpointer.append(0)
        bolpointer.append(0)
        trial.append(0)
        trial2.append(0)
        fr_irt.append(0)
        prp.append(0)
        fr_prp.append(0)
        uo_prp.append(0)

    
    #FR responses
    count0 = 0
    for i, (j, k) in izip(ba50_c.event, enumerate(frpointer)):
        if i == 120:
            count0 += 1
            frpointer[j] = count0
        if i == 200:
            count0 = -1
            frpointer[j] = count0
            count0 =0
        if i == 300:
            count0 = 0
            frpointer[j] = count0


    #FR responses B
    count0 = 0
    for i, (j, k), l in izip(ba50_c.event, enumerate(frpointerB), ba50_c.time):
        if i == 120:
            count0 += 1
            frpointerB[j] = count0
        if i > 300 or i == 130 or i < 110:
            frpointerB[j] = count0
        if i == 200:
            count0 = -1
            frpointerB[j] = count0
            count0 = 0
        if l == 0:
            count0 = 0

    #BO Right responses
    count1 = 0
    for i, (j, k) in izip(ba50_c.event, enumerate(borpointer)):
        if i == 110 or i == 130:
            count1 += 1
            borpointer[j] = count1
        if i == 410:
            count1 = 0
            borpointer[j] = count1

    #BO Left responses
    count2 = 0
    for i, (j, k) in izip(ba50_c.event, enumerate(bolpointer)):
        if i == 100:
            count2 += 1
            bolpointer[j] = count2
        if i == 410:
            count2 = 0
            bolpointer[j] = count2
    
    #trial
    count3 = 0
    for (h, i), (j, k), (l, m), (n, o) in izip(enumerate(frpointer), enumerate(trial), enumerate(runnum_c), enumerate(ratio)):
        if runnum_c[l] > runnum_c[l-1]:
            count3 = 0
        if i == 1:
            count3 += 1
        if i > -1 and i <= ratio[n]:
            trial[j] = count3
        if frpointer[h-1] == -1:
            trial[j] = 0

    #trial2
    count3 = 0
    for (i, j), (k, l), m in izip(enumerate(code), enumerate(trial2), ba50_c.time):
        if code[i-1] == 300:
            count3 += 1
        trial2[k] = count3
        if code[i] == 200 or code[i] == 300:
            trial2[k] = 0
        if m == 0:
            count3 = 0


    ba50_c = ba50_c.assign(frpointer=frpointer)   #<--------- Set the new FR Right responses array without warnings
    ba50_c = ba50_c.assign(frpointerB=frpointerB)   #<--------- Set the new FR Right responses array without warnings
    ba50_c = ba50_c.assign(borpointer=borpointer) #<--------- Set the new BO Right responses without warnings
    ba50_c = ba50_c.assign(bolpointer=bolpointer) #<--------- Set the new BO Left responses without warnings
    ba50_c = ba50_c.assign(trial=trial)           #<--------- Set the new trial count without warnings
    ba50_c = ba50_c.assign(trial2=trial2)           #<--------- Set the new trial count without warnings

    #trial
    count4 = 0
    for i, j, (k, l), m, n in izip(ba50_c.frpointer, ba50_c.frpointer.shift(), enumerate(fr_irt), ba50_c.time, ba50_c.time.shift()):
        if i > j:
            fr_irt[k] = m - n

    ba50_c = ba50_c.assign(fr_irt=fr_irt)

    for i, j, k, (l, m), (n, o), (p, q), r in izip(frpointer, fr_irt, ba50_c.event.shift(), enumerate(fr_prp), enumerate(uo_prp), enumerate(prp), ba50_c.event):
        if i == 1 and k == 300:
            fr_prp[l] = abs(2.05 - j)
            prp[p] = abs(2.05 - j)

        if k == 410 and r == 120:
            uo_prp[n] = abs(j)
            prp[p] = abs(j)

    ba50_c = ba50_c.assign(prp=prp)       #<--------- Set the new prp responses array without warnings
    ba50_c = ba50_c.assign(fr_prp=fr_prp) #<--------- Set the new fr_prp responses without warnings
    ba50_c = ba50_c.assign(uo_prp=uo_prp) #<--------- Set the new uo_prp responses without warnings
    

    ba50_c = ba50_c[['date', 'subject', 'ratio', 'runnum', 'trial', 'trial2', 'frpointer', 'frpointerB', 'borpointer', 'bolpointer', 'time', 'fr_irt', 'prp', 'fr_prp', 'uo_prp', 'event']]

    ba50_c.to_csv(outpath, index=None, sep=',')

rats = ['BA1655', 'BA1656', 'BA1657', 'BA1658']

for rat in rats:
    # wrangler(rat, RAW + '!_Subject_{}-E1.Group_1' .format(rat), RF + rat + '.csv')
    wrangler(rat, RAW + '!_Subject_{}_Experiment_FR_Unobserving.Group_1' .format(rat), RF + rat + 'TEST.csv')

