# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 20:39:23 2019
@author: Eric

read images and senor data from raspberry pi attached to the carboy


"""
from datetime import datetime
import os
import cv2
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ls = 16
#set axes labels and size
plt.rcParams['xtick.labelsize'] = ls
plt.rcParams['ytick.labelsize'] = ls

data_file = 'brew_sensor_df.csv'
pic_folder = glob.glob('brew_pic_dump/*')

df_full = pd.read_csv(data_file)

# convert time string into datetime object
time = np.array([
        datetime.strptime(t, "%a %b %d %H:%M:%S %Y") for t in df_full['time']])
# get elapsed time
elapsed = (time - time[0])
# convert to elapsed hours
elapsed = np.array([t.total_seconds() for t in elapsed])/3600

df = df_full


#%%
# 2640
# loop over each photo
for i in range(2640, len(df), 120):
    print('%i / %i' %(i+1, len(df)))
    df0 = df.iloc[:i]
    
    # change RGB channels to original
    pic0 = cv2.imread(pic_folder[int(i/120)])
    pic0 = cv2.cvtColor(pic0, cv2.COLOR_BGR2RGB)
    # crop image
    pic0 = pic0[300:, 1100:, :]
    
    fig = plt.figure()#constrained_layout=True)
    fig.set_size_inches(16, 9, forward=True)
    gs = fig.add_gridspec(6, 2)
    
    
    # plot image
    ax1 = fig.add_subplot(gs[:, 0])
    ax1.set_title('View from top of fermenter', fontsize=ls)#'View from top of fermenter'
    ax1.axis('off')
    ax1.imshow(pic0, interpolation='nearest', aspect='auto')
    
    axmq = fig.add_subplot(gs[3:, 1])
    #axmq.set_title('MQ-X gas sensor response')
    axmq.set_xlabel('Elapsed time (hours)', fontsize=ls)
    axmq.set_ylabel('MQ-X response (V)', fontsize=ls)
    axmq.set_ylim([0, 2.8])
    axmq.plot(elapsed[:i], df0['mq2'], c='c', label='MQ-2')
    axmq.plot(elapsed[:i], df0['mq3'], c='m', label='MQ-3')
    axmq.plot(elapsed[:i], df0['mq5'], c='y', label='MQ-5')
    axmq.legend(loc='upper left', ncol=3, fontsize=ls)
    
    
    axt = fig.add_subplot(gs[0, 1], sharex=axmq)
    axt.xaxis.set_visible(False)
    axt.set_ylim([26, 40])
    axt.set_title('Temperature (Temp), Pressure (P), Relative Humidity (RH), \n MQ-X gas sensor response', fontsize=ls)
    axt.plot(elapsed[:i], df0['temp'], c='r')
    axt.set_ylabel('Temp (C)', fontsize=ls)
    
    axp = fig.add_subplot(gs[1, 1], sharex=axmq)
    axp.xaxis.set_visible(False)
    axp.set_ylim([0.955, 0.985])
    axp.plot(elapsed[:i],
             (np.array(df0['press']))*9.869e-4,
             c='g')
    #axp.set_title('Pressure (?????????)')
    axp.set_ylabel('P (atm)', fontsize=ls)
    
    axrh = fig.add_subplot(gs[2, 1], sharex=axmq)
    axrh.xaxis.set_visible(False)
    axrh.set_ylim([16, 34])
    axrh.plot(elapsed[:i], df0['rh'], c='b')
    #axrh.set_title('Relative humidity (%)')
    axrh.set_ylabel('RH (%)', fontsize=ls)
    
    #axmq.axvline(x=56, color='k', alpha=0.3, linestyle='--', lw=1)

    
    
    #ax_mq.set_xlabel('Time', fontsize=16)
    
    #plt.plot(elapsed[:i], df0['temp'])

    #plt.tight_layout()
    fig.subplots_adjust(wspace=.20, hspace=0)
    plt.savefig('brew_plots\plot_'+str(i).zfill(6)+'.jpg',
                bbox_inches='tight')
    plt.show()

    
#plt.plot(time, )


'''
for i in pic_folder:
    
    # change RGB channels to original
    pic0 = cv2.imread(i)
    pic0 = cv2.cvtColor(pic0, cv2.COLOR_BGR2RGB)
    
    plt.imshow(pic0)
    plt.show()
'''