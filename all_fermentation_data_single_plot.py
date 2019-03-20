# -*- coding: utf-8 -*-
"""
Make single plot of full fermentation data
Created on Thu Mar 14 13:38:12 2019
@author: Eric
"""

from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ls = 16
#set axes labels and size
plt.rcParams['xtick.labelsize'] = ls
plt.rcParams['ytick.labelsize'] = ls

data_file = 'brew_sensor_df.csv'

df_full = pd.read_csv(data_file).iloc[0:25000]


# convert time string into datetime object
time = np.array([
        datetime.strptime(t, "%a %b %d %H:%M:%S %Y") for t in df_full['time']])
# get elapsed time
elapsed = (time - time[0])
# convert to elapsed hours
elapsed = np.array([t.total_seconds() for t in elapsed])/3600

#%%
# 2640

df0 = df_full

fig = plt.figure()#constrained_layout=True)
fig.set_size_inches(8, 8, forward=True)
gs = fig.add_gridspec(6, 1)


# plot image
ax1 = fig.add_subplot(gs[:, 0])

ax1.axis('off')
#ax1.imshow(pic0, interpolation='nearest', aspect='auto')

axmq = fig.add_subplot(gs[3:, 0])
#axmq.set_title('MQ-X gas sensor response')
axmq.set_xlabel('Elapsed time (hours)', fontsize=ls)
axmq.set_ylabel('MQ-X output (V)', fontsize=ls)
axmq.set_ylim([0, 3.4])
axmq.set_xlim([0, 100])
axmq.plot(elapsed, df0['mq2'], c='c', lw=1, label='MQ-2')
axmq.plot(elapsed, df0['mq3'], c='m', lw=1, label='MQ-3')
axmq.plot(elapsed, df0['mq5'], c='y', lw=1, label='MQ-5')
axmq.legend(loc='lower right', ncol=3, fontsize=ls-4)


axt = fig.add_subplot(gs[0, 0], sharex=axmq)
axt.xaxis.set_visible(False)
axt.set_ylim([26, 40])
axt.plot(elapsed, df0['temp'], lw=1, c='r')
axt.set_ylabel('Temp (C)', fontsize=ls, rotation=90)
axt.xaxis.set_visible(False)

pressures = np.multiply(df0['press'], 9.869e-4)
axp = fig.add_subplot(gs[1, 0], sharex=axmq)
axp.xaxis.set_visible(False)
#axp.set_ylim([0.955, 0.985])
axp.plot(elapsed, pressures, lw=1, c='g')
axp.set_ylabel('P (atm)', fontsize=ls, rotation=90)

axrh = fig.add_subplot(gs[2, 0], sharex=axmq)
axrh.xaxis.set_visible(False)
axrh.set_ylim([16, 34])
axrh.plot(elapsed, df0['rh'], lw=1, c='b')
axrh.set_ylabel('RH (%)', fontsize=ls, rotation=90)

#ax_mq.set_xlabel('Time', fontsize=16)
#plt.plot(elapsed[:i], df0['temp'])
#plt.tight_layout()
fig.subplots_adjust(wspace=.20, hspace=0)

plt.savefig(
        'C:\\Users\\Eric\\Desktop\\beer brewing manuscript\\all_data_plot.jpg',
        bbox_inches='tight',
        dpi=1000)
plt.show()

