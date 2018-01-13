'''

medPc-RF.py
This file is designed to import a Med-PC text file and reformat it into columns and rows.
KEY (pre 092117)
100: 'left'
110: 'right' 
300: 'iti'
310: 'fr5'

KEY:
    E1-3:
        100 - BO Left
        110 - BO Right
        120 - FR Left
        130 - FR Right
        200 - Pellet
        300 - Start FR
        400 - Start BO
        410 - End BO

    E4 codes:
        300 - Start FR25
        200 - Pellet FR25
        310 - Start FR100
        210 - Pellet FR100
        100 - Left  FR25
        400 - End Unobs FR25
        110 - Left  FR100
        410 - End Unobs FR100
        120 - Unobs FR25
        130 - Unbos FR100
        140 - Left  BO25
        150 - Left  BO100
        160 - Right BO25
        170 - Right BO100
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
RAW = MAINDIR + 'MedPC-Data/' + 'Exp4/'
RF = MAINDIR + 'RF/' + 'Exp 4/'
RF2 = MAINDIR + 'RF2/'
SUMS = 'Sums/'

HEADER = ['DATE', 'SUBJECT', 'INDEX', 'TIME_CODE']

files = []
rats = []
rundates = []
#=============================================Start Code===========================================
#==========================================Convert to .CSV=========================================

def wrangler(inname, inpath, outpath):
    if os.path.exists(outpath):
        os.remove(outpath)
    else:
        pass

    data = pd.read_table(inpath, skiprows=[0], header=None, index_col=False)

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

    for i in data[0]:
        if 'Start Date:' in i:
            date.append(i[12:])
        if 'Subject' in i:
            subject.append(i[9:])
        if 'A:' in i:
            a_array.append(i[0])
        if 'C:' in i:
            c_array.append(i[0])

    data = data[(data[0].str.contains('Start Date:') == False)&
                (data[0].str.contains('End Date:') == False)&
                (data[0].str.contains('Subject:') == False)&
                (data[0].str.contains('Experiment:') == False)&
                (data[0].str.contains('Group:') == False)&
                (data[0].str.contains('Box:') == False)&
                (data[0].str.contains('Start Time:') == False)&
                (data[0].str.contains('End Time:') == False)&
                (data[0].str.contains('MSN:') == False)]

    for i in data[0]:
        if '-' in i or 'A' in i or '0.000' in i:
            arrayType.append(1)
        elif '-' not in i or 'C' in i:
            arrayType.append(2)

    # arrayType = pd.Series(arrayType)
    data['arrayType'] = arrayType

    data_a = data[data.arrayType == 1]
    data_c = data[data.arrayType == 2]

    count_a = -1

    for i in data_a[0]:
        if 'A' in i:
            count_a +=1
        runnum_a.append(count_a)

    count_c = -1
    for i in data_c[0]:
        if 'C' in i:
            count_c +=1
        runnum_c.append(count_c)

    # data_a = data_a.assign(runnum=runnum_a) #<--------- Set the new runnum array without warnings
    data_c = data_c.assign(runnum=runnum_c)   #<--------- Set the new runnum array without warnings

    data_a = data_a[data[0].str.contains('A:') == False]

    for i in data_a[0]:
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
    for i, (j, k) in izip(data_c.runnum.shift(), enumerate(data_c.runnum)):
        if i == k:
            datecol[j] = date[idx]
            ratio[j] = FR[idx]
        if i != k:
            idx += 1

    data_c = data_c.assign(date=datecol) #<--------- Set the new date array without warnings
    data_c = data_c.assign(subject=subj) #<--------- Set the new subject name array without warnings
    data_c = data_c.assign(ratio=ratio)  #<--------- Set the new date array without warnings

    data_c = data_c[data_c.date != '12/27/17'] #<--- Drop the first Run

    data_c = data_c[data_c[0].str.contains('C:') == False]
    time_code = []
    time = []
    code = []

    for i in data_c[0]:
        time_code.append(i.strip().split(':')[1].strip())

    for i in time_code:
        time.append(int(i.strip().split('.')[0])/100)
        code.append(int(i.strip().split('.')[1]))

    data_c = data_c.assign(time=time)  #<--------- Set the new time array without warnings
    data_c = data_c.assign(event=code) #<--------- Set the new code array without warnings

    frpointer25, frpointer100 = [], []
    borpointer25, borpointer100 = [], []
    bolpointer = []
    frval = []

    fr_irt25, fr_irt100 = [], []
    fr_prp, fr_prp = [], []
    uo_prp = []
    prp25, prp100 = [], []

    trial, trial25, trial100  = [], [], []

    #initialize pointers
    for i in data_c.event:
        frpointer25.append(0)
        frpointer100.append(0)

        borpointer25.append(0)
        borpointer100.append(0)
        bolpointer.append(0)

        trial.append(0)
        trial25.append(0)
        trial100.append(0)

        fr_irt25.append(0)
        fr_irt100.append(0)
        
        prp25.append(0)
        prp100.append(0)

        fr_prp.append(0)
        uo_prp.append(0)
        frval.append(0)

    #FR25 responses
    count0 = 0
    for i, (j, k) in izip(data_c.event, enumerate(frpointer25)):
        if i == 100:                                      #<--- 100 - Left FR25
            count0 += 1
            frpointer25[j] = count0
        if i == 400 or i == 120 or i == 140 or i == 160: #<--- 400 - Unobs FR25, 120 - Unobs FR25, 140 - Left BO25, 160 - End Right BO25
            frpointer25[j] = count0
        if i == 200:                                      #<--- 200 - Pellet FR25
            frpointer25[j] = -1
            count0 =0
        if i == 300:                                      #<--- 300 - Start FR25
            frpointer25[j] = 0
        elif i != 100 and i != 120 and i != 140 and i != 160 and i != 200 and i != 300 and i != 400:
            frpointer25[j] = 'nan'

    #FR100 responses
    count0 = 0
    for i, (j, k) in izip(data_c.event, enumerate(frpointer100)):
        if i == 110:                                     #<--- 110 - Left  FR100
            count0 += 1
            frpointer100[j] = count0
        if i == 410 or i == 130 or i == 150 or i == 170: #<--- 410 - Unobs FR100, 130 - Unbos FR100, 150 - Left BO100, 170 - End Right BO100
            frpointer100[j] = count0
        if i == 210:                                     #<--- 210 - Pellet FR100
            frpointer100[j] = -1
            count0 =0
        if i == 310:                                     #<--- 310 - Start FR100
            frpointer100[j] = 0
        elif i != 110 and i != 210 and i != 310 and i != 410 and i != 130 and i != 150 and i != 170:
            frpointer100[j] = 'nan'

    #BO25 Right responses
    count1 = 0
    for i, (j, k) in izip(data_c.event, enumerate(borpointer25)):
        if i == 120 or i == 140:
            count1 += 1
            borpointer25[j] = count1
        if i == 400 or i == 160:
            borpointer25[j] = 0
        elif i != 120 and i != 140 and i != 400 and i != 160:
            borpointer25[j] = 'nan'

    #BO100 Right responses
    count1 = 0
    for i, (j, k) in izip(data_c.event, enumerate(borpointer100)):
        if i == 130 or i == 150:
            count1 += 1
            borpointer100[j] = count1
        if i == 410 or i == 170:
            borpointer100[j] = 0
        elif i != 130 and i != 150 and i != 410 and i != 170:
            borpointer100[j] = 'nan'

    #trial
    count = 0
    for (i, j), (k, l), m in izip(enumerate(code), enumerate(trial), data_c.time):
        if code[i-1] == 300 or code[i-1] == 310 or code[i-1] == 200 or code[i-1] == 210:
            count += 1
        trial[k] = count
        # if code[i] == 200 or code[i] == 200 or code[i] == 300 or code[i] == 310:
        #     trial[k] = 0
        if m == 0:
            count = 0
   
    #trial25
    count = 0
    for (i, j), (k, l), m in izip(enumerate(frpointer25), enumerate(trial25), data_c.time):
        if frpointer25[i] == 1 or frpointer25[i] == 0:   
            count += 1
        trial25[k] = count
        if frpointer25[i] == 'nan':
            trial25[k] = 'nan'
        if m == 0:
            count = 0    

    #trial100
    count = 0
    for (i, j), (k, l), m in izip(enumerate(frpointer100), enumerate(trial100), data_c.time):
        if frpointer100[i-1] != 1 and frpointer100[i] == 0:
            count += 1        
        if frpointer100[i] == 1 and frpointer100[i-1] != 0:
            count += 1
        trial100[k] = count
        if frpointer100[i] == 'nan':
            trial100[k] = 'nan'
        if m == 0:
            count = 0    

    #FR Value
    count = 0
    for (i, j), (k, l), m in izip(enumerate(frpointer25), enumerate(frval), ratio):
        if frpointer25[i] != 'nan':
            frval[k] = 25
        else:
            frval[k] = 100

    data_c = data_c.assign(frpointer25=frpointer25)   #<--------- Set the new FR Right responses array without warnings
    data_c = data_c.assign(frpointer100=frpointer100)   #<--------- Set the new FR Right responses array without warnings
    data_c = data_c.assign(borpointer25=borpointer25) #<--------- Set the new BO Right responses without warnings
    data_c = data_c.assign(borpointer100=borpointer100) #<--------- Set the new BO Right responses without warnings
    data_c = data_c.assign(trial=trial)           #<--------- Set the new trial count without warnings
    data_c = data_c.assign(trial25=trial25)           #<--------- Set the new trial count without warnings
    data_c = data_c.assign(trial100=trial100)           #<--------- Set the new trial count without warnings
    data_c = data_c.assign(frval=frval)

    #fr_irt25
    count4 = 0
    for i, j, (k, l), m, n in izip(data_c.frpointer25, data_c.frpointer25.shift(), enumerate(fr_irt25), data_c.time, data_c.time.shift()):
        if i > j and i > 1 and i != 'nan' and m > 0:
            fr_irt25[k] = m - n
        else:
            fr_irt25[k] = 'nan'

    #fr_irt100
    count4 = 0
    for i, j, (k, l), m, n in izip(data_c.frpointer100, data_c.frpointer100.shift(), enumerate(fr_irt100), data_c.time, data_c.time.shift()):
        if i > j and i > 1 and m > 0:
            fr_irt100[k] = m - n
        else:
            fr_irt100[k] = 'nan'

    #prp25
    for i, j, (k, l), m, n in izip(data_c.frpointer25, data_c.frpointer25.shift(-1), enumerate(prp25), data_c.time, data_c.time.shift(-1)):
        if i == -1 and j == 1:
            prp25[k] = (m - n)*-1
        else:
            prp25[k] = 'nan'

    #prp100
    for i, j, (k, l), m, n in izip(data_c.frpointer100, data_c.frpointer100.shift(-1), enumerate(prp100), data_c.time, data_c.time.shift(-1)):
        if i == -1 and j == 1:
            prp100[k] = (m - n)*-1
        else:
            prp100[k] = 'nan'

    data_c = data_c.assign(fr_irt25=fr_irt25)
    data_c = data_c.assign(fr_irt100=fr_irt100)
    data_c = data_c.assign(prp25=prp25)
    data_c = data_c.assign(prp100=prp100)

    data_c = data_c[['date', 'subject', 'time', 'event', 'runnum', 'frval', 'frpointer25', 'frpointer100', 'borpointer25', 'borpointer100', 'trial', 'trial25', 'trial100', 'fr_irt25', 'fr_irt100', 'prp25', 'prp100']]# 'trial2', 'borpointer2', 'bolpointer', 'fr_prp', 'uo_prp']]

    data_c.to_csv(outpath, index=None, sep=',')

rats = ['BA1655', 'BA1656', 'BA1657', 'BA1658']

for rat in rats:
    wrangler(rat, RAW + '!_Subject_{}_Experiment_FR_Unobserving_E4.Group_1' .format(rat), RF + rat + '_C.csv')



def wrangler_a(inname, inpath, outpath):
    if os.path.exists(outpath):
        os.remove(outpath)
    else:
        pass

    data = pd.read_table(inpath, skiprows=[0], header=None, index_col=False)

    date = []
    subject = []
    subj = [] #<---Delete maybe?
    a_array = []

    arrayType = []
    datecol = []
    runnum_a = []

    FR25_Resp = []
    FR100_Resp = []
    FR25_rfr = []
    FR100_rfr = []
    FR25_Time = []
    FR100_Time = []
    FR25_Unobs = []
    FR100_Unobs = []

    for i in data[0]:
        if 'Start Date:' in i:
            date.append(i[12:])
        if 'Subject' in i:
            subject.append(i[9:])
        if 'A:' in i:
            a_array.append(i[0])

    data = data[(data[0].str.contains('Start Date:') == False)&
                (data[0].str.contains('End Date:') == False)&
                (data[0].str.contains('Subject:') == False)&
                (data[0].str.contains('Experiment:') == False)&
                (data[0].str.contains('Group:') == False)&
                (data[0].str.contains('Box:') == False)&
                (data[0].str.contains('Start Time:') == False)&
                (data[0].str.contains('End Time:') == False)&
                (data[0].str.contains('MSN:') == False)]

    for i in data[0]:
        if '-' in i or 'A' in i or '0.000' in i:
            arrayType.append(1)
        elif '-' not in i or 'C' in i:
            arrayType.append(2)

    data['arrayType'] = arrayType

    data_a = data[data.arrayType == 1]
    
    data_a.columns = ['maindata', 'arrayType']

    count = 0
    for i in data_a['maindata']:
        if 'A' in i:
            count +=1
        runnum_a.append(count)

    data_a = data_a.assign(runnum=runnum_a) #<--------- Set the new runnum array without warnings

    data_a = data_a[data_a['maindata'].str.contains('A:') == False]

    for i in data_a['maindata']:
        datecol.append(date[0])
        subj.append(subject[0])

    data_a = data_a.assign(date=datecol)
    data_a = data_a.assign(subj=subj)

    maindata = []
    for i in data_a['maindata']:
        maindata.append(i)

    vals = []
    for i in maindata:
        data = i[5:].replace(" ", "").strip(' ').split(':')
        data = float(data[1])*-1
        vals.append(data)

    data_a['maindata'] = vals

    for i, j in enumerate(maindata):
        if '0:' in j:
            FR25_Resp.append(float(j[5:].replace(" ", "").strip(' ').split(':')[1])*-1)
        if '1:' in j:
            FR100_Resp.append(float(j[5:].replace(" ", "").strip(' ').split(':')[1])*-1)
        if '2:' in j:
            FR25_rfr.append(float(j[5:].replace(" ", "").strip(' ').split(':')[1])*-1)
        if '3:' in j:
            FR100_rfr.append(float(j[5:].replace(" ", "").strip(' ').split(':')[1])*-1)
        if '4:' in j:
            FR25_Time.append(float(j[5:].replace(" ", "").strip(' ').split(':')[1])*-1)
            print j
        if '5:' in j:
            FR100_Time.append(float(j[5:].replace(" ", "").strip(' ').split(':')[1])*-1)
            print j
        if '6:' in j:
            FR25_Unobs.append(float(j[5:].replace(" ", "").strip(' ').split(':')[1])*-1)
        if '7:' in j:
            FR100_Unobs.append(float(j[5:].replace(" ", "").strip(' ').split(':')[1])*-1)
        # print FR25_Time, FR100_Time

    dset_a = pd.DataFrame()
    dset_a = dset_a.assign(FR25_Resp=FR25_Resp)     #<------- A(0)
    dset_a = dset_a.assign(FR100_Resp=FR100_Resp)   #<------- A(1)
    dset_a = dset_a.assign(FR25_rfr=FR25_rfr)       #<------- A(2)
    dset_a = dset_a.assign(FR100_rfr=FR100_rfr)     #<------- A(3)
    dset_a = dset_a.assign(FR25_Time=FR25_Time)     #<------- A(4)
    dset_a = dset_a.assign(FR100_Time=FR100_Time)   #<------- A(5)
    dset_a = dset_a.assign(FR25_Unobs=FR25_Unobs)   #<------- A(6)
    dset_a = dset_a.assign(FR100_Unobs=FR100_Unobs) #<------- A(7)
    dset_a = dset_a.assign(runnum=set(runnum_a))
    dset_a = dset_a.assign(date=date)
    dset_a = dset_a[dset_a.date != '12/27/17']

    dset_a['p_BO|FR25'] = ((dset_a.FR25_Unobs)/dset_a.FR25_Time)*100
    dset_a['p_BO|FR100'] = ((dset_a.FR100_Unobs)/dset_a.FR100_Time)*100

    # dset_a = dset_a.replace(dset_a[dset_a.date == '1/08/18'].all(), np.nan)
    # for row in dset_a.itertuples():
        # if row.date == '01/08/18':
            # dset_a = dset_a.replace(row, np.nan)

    dset_a = dset_a[['date', 'runnum', 'FR25_Resp', 'FR100_Resp', 'FR25_rfr', 'FR100_rfr', 'FR25_Time', 'FR100_Time', 'FR25_Unobs', 'FR100_Unobs', 'p_BO|FR25', 'p_BO|FR100']]

    dset_a.to_csv(outpath, index=None, sep=',')

rats = ['BA1655', 'BA1656', 'BA1657', 'BA1658']

for rat in rats:
    wrangler_a(rat, RAW + '!_Subject_{}_Experiment_FR_Unobserving_E4.Group_1' .format(rat), RF + rat + '_A.csv')


