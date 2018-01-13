'''
event key:
    300 - Start FR25
    200 - Pellet FR25
    100 - Left  FR25
    400 - End Unobs FR25
    120 - Unobs FR25
    140 - Left  BO25
    160 - Right BO25

    310 - Start FR100
    210 - Pellet FR100
    110 - Left  FR100
    410 - End Unobs FR100
    130 - Unbos FR100
    150 - Left  BO100
    170 - Right BO100
'''
from __future__ import division

import pandas as pd
import numpy as np
from itertools import izip

from matplotlib import pyplot as plt


MAINDIR = '/Users/benjaminlibman/Google Drive/Academics/CMU/Lab/Research/Unobserving/Data/'
RAW = MAINDIR + 'MedPC-Data/'
# RF = MAINDIR + 'RF/' + 'Exp 4/'
RF = '/Users/benjaminlibman/Google Drive/Academics/CMU/Lab/Research/Unobserving/Data/RF/Exp 4/'
# RF2 = MAINDIR + 'RF2/'
SUMS = MAINDIR + 'Sums/' + 'Exp 4/'
FIGS = '/Users/benjaminlibman/Google Drive/Academics/CMU/Lab/Research/Unobserving/Figures/Exp 4/'
CRECS = FIGS + 'crecs/'

def cumrec(inname, inpath, outpath):
    dset = pd.read_csv(inpath, sep=',', header=0, index_col=None)
    
    for date, run in zip(set(dset.date), set(dset.runnum)):
        for ratio in sorted(set(dset.frval[dset.frval > 0])):
            thisRun = run
            data = dset[dset.runnum == thisRun]#int('{}'.format(run))

            print 'Doing {} - {}' .format(inname, data.date.iloc[1])

            ycol = []
            pellets25 = []
            pellets100 = []
            toi25 = []
            toi100 = []
            tor25 = []
            tor100 = []
            frmain = []
            frr25 = []
            frr100 = []

            for i in data.time:
                ycol.append(None)
                pellets25.append(None)
                pellets100.append(None)
                toi25.append(None)
                toi100.append(None)
                tor25.append(None)
                tor100.append(None)
                frmain.append(None)
                frr25.append(None)
                frr100.append(None)

            for (i, j), (k, l) in zip(enumerate(data.time), enumerate(frmain)):
                frmain[k] = j #<----All resps    
                                                                                          # h, i                 j, z                     k, l               m, n              o, p                      q, r                s, t
            for (h, i), (j, z), (k, l), (m, n), (o, p), (q, r) in zip(enumerate(data.time), enumerate(data.event), enumerate(pellets25), enumerate(toi25), enumerate(tor25), enumerate(frr25)):
                if z == 300 or z == 100: #<---Start FR25 and FR25 Resp
                    frr25[q] = i
                if z == 200: #<---FR25 pellet
                    pellets25[k] = i
                if z == 120 or z == 400: #<---FR25 Start and end BO
                    toi25[m] = i
                if z == 140 or z == 160: #<---FR25 BO Resp  Left and Right
                    tor25[o] = i

            for (h, i), (j, z), (k, l), (m, n), (o, p), (q, r) in zip(enumerate(data.time), enumerate(data.event), enumerate(pellets100), enumerate(toi100), enumerate(tor100), enumerate(frr100)):
                if z == 310 or z == 110: #<---Start FR100 and FR100 Resp
                    frr100[q] = i 
                if z == 210: #<---FR100 pellet
                    pellets100[k] = i
                if z == 130 or z == 410: #<---FR100 Start and end BO
                    toi100[m] = i
                if z == 150 or z == 170: #<---FR100 BO Resp  Left and Right
                    tor100[o] = i

            ycount = 0
            for (j, k) in enumerate(ycol):
                if ycount <= 300:
                    ycount += 1
                    ycol[j] = ycount
                if ycount == 301:
                    ycount = 0
                    ycol[j] = ycount
        
        fig, ax = plt.subplots(figsize=(10, 7.5))

        cr_frr = plt.plot(frmain, ycol, 'y-', label='PRP')
        cr_frr = plt.plot(frr25, ycol, 'k-', label='FR25')
        cr_frr = plt.plot(frr100, ycol, 'b-', label='FR100')
        cr_sr = plt.plot(pellets25, ycol, 'k-', marker=(1, 1, 240), label='FR25 Sr', markersize=8)
        cr_sr = plt.plot(pellets100, ycol, 'b-', marker=(1, 1, 240), label='FR100 Sr', markersize=8)
        cr_toi = plt.plot(toi25, ycol, 'r|-', label='FR25 TO', markersize=8)
        cr_toi = plt.plot(toi100, ycol, 'g|-', label='FR100 TO', markersize=8)
        cr_tor = plt.plot(tor25, ycol, 'ro-', label='FR25 TO Resp', markersize=4)
        cr_tor = plt.plot(tor100, ycol, 'go-', label='FR100 Resp', markersize=4)
        
        xval = []
        for i, j, k, l, m in zip(frmain, frr100, pellets100, tor100, toi100):
            if i == j or i == k or i == l or i == m:
                xval.append(i)
        
        ax.axvspan(xmin=min(xval), xmax=max(xval), ymin=0, ymax=300, facecolor='grey', alpha=1)
        xval = []

        plt.suptitle('{} Cumulative Record'.format(inname))
        ax.set_title(str(data.date.iloc[1]))

        plt.tick_params(axis='both', direction='out', labelsize=8)


        plt.legend(loc=3, fontsize=8, shadow=False, bbox_to_anchor=(1, 0.5))
        plt.xlim(-.5)
        plt.ylim(-.5, 301)
        fig.set_size_inches(10, 7.5, forward=True)

        plt.savefig(CRECS + rat + '-{}-crec-E4.png'.format(str(run)), dpi=300)

        plt.close(fig)

        crec = pd.DataFrame()

        crec = crec.assign(ycol=ycol)
        crec = crec.assign(frmain=frmain)
        crec = crec.assign(frr25=frr25)
        crec = crec.assign(frr100=frr100)
        crec = crec.assign(pellets25=pellets25)
        crec = crec.assign(pellets100=pellets100)
        crec = crec.assign(toi25=toi25)
        crec = crec.assign(toi100=toi100)
        crec = crec.assign(tor25=tor25)
        crec = crec.assign(tor100=tor100)

        crec = crec[['ycol','frmain', 'frr25', 'frr100', 'pellets25', 'pellets100', 'toi25', 'toi100', 'tor25', 'tor100']]
        crec.to_csv(CRECS + 'crecs-CSV/' + rat + '-{}-crec-E4.csv'.format(str(run)), index=None, sep=',')


rats = ['BA1655']#, 'BA1656', 'BA1657', 'BA1658']

for rat in rats:
    cumrec(rat, RF + rat + '_C.csv' .format(rat), None)
