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
from itertools import izip

MAINDIR = '/Users/benjaminlibman/Google Drive/Academics/CMU/Lab/Research/Unobserving/Data/'
RAW = MAINDIR + 'MedPC-Data/'
# RF = MAINDIR + 'RF/' + 'Exp 3/'
RF = '/Users/benjaminlibman/Google Drive/Academics/CMU/Lab/Research/Unobserving/Data/RF/Exp 3/'
# RF2 = MAINDIR + 'RF2/'
SUMS = MAINDIR + 'Sums/' + 'Exp 3/'

def summary(inname, inpath, outpath):
    dset = pd.read_csv(inpath, sep=',', header=0, index_col=None)
    # dset = dset[dset.runnum > 24]
    # dset.runnum = dset.runnum - 24

    sumed = pd.DataFrame()

    date = []
    trial = []
    fr = []
    max_fr = []
    pellets = []
    fr_irt = []
    uor_irt = []
    uol_irt = []
    timeouts = []
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
    c_ratio = []
    uo_fr_resps = []
    uo_uo_resps = []
    p_to = []
    p_to_sr = []
    sr_rate = []
    iri = []



    for run in set(dset.runnum):
        for ratio in sorted(set(dset.frval[dset.frval > 0])):
            c_ratio.append(0)
            thisRun = run
            data = dset[dset.runnum == thisRun]#int('{}'.format(run))
            sr = max(set(data.frpointer))
            # fr_irt.append(round(np.mean(data.fr_irt[(data.frpointer > 1)&(data.frval == ratio)]), 3))
            date.append(data.date.iloc[1])
            trial.append(ratio/25)
            fr.append(ratio)

            pellets.append(len(data[data.frpointer == sr]))
            max_fr.append(max(data.frval))

            if sum(data.fr_irt[(data.frpointer > 1)&(data.frval == ratio)]) > 0:
                timeouts.append(len(data.event[(data.event == 400)&(data.frval == ratio)]))
                fr_prp.append(np.mean(data.fr_prp[(data.fr_prp > 0)&(data.time.shift() > 0)&(data.frval == ratio)]))
                uo_prp.append(np.mean(data.uo_prp[(data.uo_prp > 0)&(data.time.shift() > 0)&(data.frval == ratio)]))
                uo_fr_resps.append(len(data.event[(data.event == 100)&(data.frval == ratio)]))
                uo_uo_resps.append(len(data.event[(data.event == 110)&(data.frval == ratio)]))
                uo_resps.append(len(data.event[(data.event == 100)&(data.frval == ratio)]) + len(data.event[(data.event == 110)&(data.frval == ratio)]))
                sr_rate.append(round((len(data.event[(data.event == 200)])/sum(data.fr_irt[(data.frpointer > 1)&(data.frval == ratio)]))*60, 3))
                iri.append(round(1/((len(data.event[(data.event == 200)])/sum(data.fr_irt[(data.frpointer > 1)&(data.frval == ratio)]))), 3))
                p_to.append(round(len(data.event[(data.event == 400)&(data.frval == ratio)])/(len(data.frpointer[data.frpointer == 1])), 4))
                p_to_sr.append(round(len(data.event[(data.event == 400)&(data.frval == ratio)])/(len(data.event[(data.event == 200)])), 5))
            else:
                timeouts.append('*')
                fr_prp.append('*')
                uo_prp.append('*')
                uo_fr_resps.append('*')
                uo_uo_resps.append('*')
                uo_resps.append('*')
                sr_rate.append('*')
                iri.append('*')
                p_to.append('*')
                p_to_sr.append('*')

            if sum(data.fr_irt[(data.frpointer.shift() > 0)&(data.frval == ratio)]) > 0:
                fr_runrate.append(round((len(data.event[(data.event == 120)&(data.frval == ratio)])/sum(data.fr_irt[(data.frpointer.shift() > 0)&(data.frval == ratio)]))*60, 3))
            else:
                fr_runrate.append('*')


        
    sumed = sumed.assign(date=date)
    sumed = sumed.assign(trial=trial)
    sumed = sumed.assign(fr=fr)
    sumed = sumed.assign(timeouts=timeouts)
    sumed = sumed.assign(fr_prp=fr_prp)
    sumed = sumed.assign(uo_prp=uo_prp)
    sumed = sumed.assign(localrate=fr_runrate)
    sumed = sumed.assign(uo_resps=uo_resps)
    sumed = sumed.assign(uo_fr_resps=uo_fr_resps)
    sumed = sumed.assign(uo_uo_resps=uo_uo_resps)
    sumed = sumed.assign(p_to=p_to)
    sumed = sumed.assign(p_to_sr=p_to_sr)
    sumed = sumed.assign(sr_rate=sr_rate)
    sumed = sumed.assign(iri=iri)
    sumed = sumed.assign(max_fr=max_fr)
    
    sumed = sumed[['date', 'trial', 'fr', 'fr_prp', 'uo_prp', 'uo_resps', 'uo_fr_resps' , 'uo_uo_resps', 'localrate', 'timeouts', 'p_to', 'p_to_sr', 'sr_rate', 'iri', 'max_fr']]

    sumed.to_csv(outpath, index=None, sep=',')
    
rats = ['BA1655', 'BA1656', 'BA1657', 'BA1658']

for rat in rats:
    summary(rat, RF + rat + '.csv' .format(rat), SUMS + rat + 'sums-E3.csv')
