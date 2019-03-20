import numpy as np
import pandas as pd
import time
from picamera import PiCamera
import bme280
import spidev

# open connection to SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
def read_mcp_all():
    #read SPI data from MCP3008 analog to digital converter.
    #Returns voltage of each channel and returns list
    #assuming a 3.3V input.
    all_output = []
    #iterate through each channel and read voltage
    for ch in range(8):
        adc = spi.xfer2([1,(8+ch)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        volts = ((data*3.3)/float(1023))
        all_output.append(volts)
    return all_output


#set up camera
pic_folder = '/media/pi/KINGSTON/pic_dump/pic_'
cam = PiCamera()
cam.resolution = (2592, 1944)
cam.framerate = 15
#cam.rotation = 270




#number of data points to collect over time
loop_num = 100000

df = pd.DataFrame(
	data=np.zeros((loop_num,7)),
	columns=['time', 'temp', 'press',
		'rh', 'mq2', 'mq3', 'mq5'])

save_df_path = '/media/pi/KINGSTON/sensor_df.csv'


for i in range(loop_num):
	print('%i / %i' %(i+1, loop_num))

	#read BME280
	temp, press, rh = bme280.readBME280All()
	temp_f = temp*(9/5) + 32
	
	#read MCP3008 ADC
	mcp_output = read_mcp_all()
	mq2, mq3, mq5 = mcp_output[0], mcp_output[1], mcp_output[2]

	#print results
	print(time.ctime())
	print('temp (C), (F): '+format(temp)+', '+format(temp_f))
	print('pressure (hPa): '+format(press))
	print('humidity (%): '+format(rh))

	print('MQ-X sensors: '+format(
		np.around([mq2, mq3, mq5], decimals=5)))

	df.iloc[i] = [time.ctime(), temp, press, rh,
			mq2, mq3, mq5]



	#every nth point, take a picture
	take_pics = True
	if i%120==0 and take_pics:

	
		pic_num = str(i).zfill(5)
		cam.start_preview()
		time.sleep(2)
		cam.capture(pic_folder+pic_num+'.jpg')
		cam.stop_preview()
		time.sleep(12.5)

	else:
		time.sleep(15)

	#remove empty rows before writing to file
	df[df['time']!=0].to_csv(save_df_path, index=False)
