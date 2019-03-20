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

print(read_mcp_all())
