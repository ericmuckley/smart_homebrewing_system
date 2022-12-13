# Smart homebrewing system
Code for monitoring fermentation of home-brewed beer using a Raspberry Pi computer, sensors and a camera.

Video of dynamic real-time data streaming is available at
https://youtu.be/_vpxnixSp3A

## Description of files
* **all_fermentation_single_plot.py**: Python script to plot all sensor data from "brew_sensor_df.csv" in a single plot.
* **bme280.py**: Python script for reading temperature, pressure, and relative humidity data from BME280 sensor.
* **brew_sensor_df.csv**: CSV file of all sensor data collected during fermentation process.
* **convert_images_to_vid.py**: Python script for converting a folder of images (or plots) into a timelapse video.
* **plots_of_fermentation_data.py**: Python script for creating plots of sensor data with embedded images from camera.
* **read_from_rpi.py**: Python script for streaming sensor data live from Rapberry Pi over Wifi to local PC.
* **read_mcp3008.py**: Python script for reading multi-channel output from MCP3008 analog to digital converter.
* **read_sensors.py**: Python script running on Raspberry Pi which collects data from sensors, controls camera, and saved data to file.
