# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 16:15:06 2019

@author: ericmuckley@gmail.com
"""
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

ls = 16
#set axes labels and size
plt.rcParams['xtick.labelsize'] = ls
plt.rcParams['ytick.labelsize'] = ls



def open_ssh_tunnel(rpi_ip='RPI_IP_ADDRESS',
                    key_file_path='PATH_TO_PRIVATE_KEY_FILE.pem'):
    '''Open a connection to rpi using the
    IP address and a path to the .pem private key file for the rpi.
    Example inputs:
        rpi_ip = '172.22.5.231'    
        key_file_path = 'C:\\Users\\a6q\\tf-container.pem'
    Returns an SSH session instance.
    '''
    import paramiko
    k = paramiko.RSAKey.from_private_key_file(key_file_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(hostname=cades_ip, username='cades', pkey=k)
    return ssh



def open_ssh_w_password(ip='RPI_IP_ADDRESS',
                        username='pi',
                        password='PASSWORD'):
    import paramiko
    #k = paramiko.RSAKey.from_private_key_file(key_file_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(hostname=ip, username=username, password=password)
    return ssh


def send_to_pi(ssh, local_file_path, pi_file_path):
    '''Send a local file to rpi.
    Example inputs:
        ssh = open_ssh_tunnel(cades_ip, key_file_path)
        local_file_path = 'C:\\Users\\a6q\\exp_data\\my_text.txt'
        cades_file_path = '/home/pi/my_text.txt'
    '''
    ftp = ssh.open_sftp()
    ftp.put(local_file_path, pi_file_path)
    ftp.close()



def pull_from_pi(ssh, local_file_path, pi_file_path):
    '''Pull a file from rpi onto local PC.
    Example inputs:
        ssh = open_ssh_tunnel(rpi_ip, key_file_path)    
        local_file_path = 'C:\\Users\\a6q\\exp_data\\my_text.txt'
        pi_file_path = '/home/pi/my_text.txt'
    '''
    ftp = ssh.open_sftp()
    ftp.get(cades_file_path, local_file_path)
    ftp.close()

def run_script_on_rpi(ssh, rpi_script_path):
    '''Run a Python script on rpi from the local PC and 
    prints the output and errors from the script.
    Example inputs:
        ssh = open_ssh_tunnel(rpi_ip, key_file_path)    
        rpi_script_path = '/home/pi/scripts/my_python_script.py'
    '''
    stdin, stdout, stderr = ssh.exec_command('python '+pi_script_path)
    [print(line) for line in stdout.readlines()]
    [print(line) for line in stderr.readlines()]
    
    

#collect data from rpi over SSH
file_to_pull = '/media/pi/KINGSTON/sensor_df.csv'
destination_file = 'C:\\Users\\Eric\\sensor_data_from_rpi.csv'

ssh = open_ssh_w_password()




for i in range(5):
    print(i)

    try:
        pull_from_pi(ssh, destination_file, file_to_pull)
        df = pd.read_csv(destination_file)
            
        #plot sensor output over time
        fig, (ax_temp, ax_press, ax_rh, ax_mq) = plt.subplots(4, sharex=True)
        fig.set_size_inches(9, 7, forward=True)
    
        t = [datetime.strptime(
                time0, "%a %b %d %H:%M:%S %Y") for time0 in df['time']]
    
        ax_temp.plot(t, df['temp'].astype(float)*(9/5)+32, c='r')
        ax_press.plot(t, df['press'].astype(float), c='k')
        ax_rh.plot(t, df['rh'].astype(float))
    
        for col in df.columns[4:]:
            ax_mq.plot(t, df[col].astype(float), label=col)
    
        ax_mq.set_xlabel('Time', fontsize=16)
        ax_temp.set_ylabel('Temp. (F)', fontsize=ls)
        ax_press.set_ylabel('Press.', fontsize=ls)
        ax_rh.set_ylabel('RH (%)', fontsize=16)
        ax_mq.set_ylabel('MQ-X (V)', fontsize=ls)
    
        ax_mq.legend(fontsize=8, loc='upper left')
        #plt.tight_layout()
        #plt.subplots_adjust()
        plt.xticks(rotation=90)
        plt.show()
        
    except:
        pass

    time.sleep(2)


