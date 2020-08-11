# -*- coding: utf-8 -*

"""
Created on Sat May 18 10:35:36 2019

@author: mark
"""

import os
import datetime as dt
import time
import sqlite3
import bme680 # sudo pip3 install bme680
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
import smbus
import numpy as np


dataDB = 'dataDB.sqlite3'

## Initalize Display
i2c = busio.I2C(3, 2) # Create the I2C interface with SCL = 3, SDA = 2.
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c) # Create the SSD1306 OLED class. pixel width/height
width = disp.width
height = disp.height
image = Image.new('1', (width, height)) # Create blank image for drawing.
draw = ImageDraw.Draw(image) # Get drawing object to draw on image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
font = ImageFont.load_default() # Load default font.


""" Initialisierung BME680
 i2c auf Standardkonfiguration: SMBus(1) SDA=GPIO2=Pin3 und SCL=GPIO3=Pin5
 i2c auf SMBus(2) SDA=GPIO23=Pin16 und SCL=GPIO24=Pin18. Muss beim Rasperry Pi konfiguriert werden unter /boot/config.txt:
 dtoverlay=i2c-gpio,bus=2,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24
"""
smbus2 = smbus.SMBus(2)
sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY, smbus2)
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


# ## Starten des Django Entwicklungsservers
print('warte auf IP-Adresse...')
time.sleep(5) 
try:
    ipAll = subprocess.check_output('hostname -I', shell=True).decode('utf-8')
    ip = ipAll[0:ipAll.find(' ')]
    subprocess.Popen(['python3', 'manage.py', 'runserver', ip+':8000'])
except:
    print('Django nicht gestartet')  


i=0
while True:  
    i = i+1
    # Sensor    
    sensor.get_sensor_data()
    temp = sensor.data.temperature
    humi = sensor.data.humidity
    prea = sensor.data.pressure
    vocR = sensor.data.gas_resistance/10000 # 10kOhm = 10kOhm
    if i < 5:
        vocR = 8
    
         
    zeit = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Display
    ipAll = subprocess.check_output('hostname -I', shell=True).decode('utf-8')
    ip = ipAll[0:ipAll.find(' ')]
    top = -2
    draw.rectangle((0, 0, width, height), outline=0, fill=0) # Draw a black filled box to clear the image.
    draw.text((0, top+0),'IP: %s' %ip , font=font, fill=255)
    draw.text((0, top+8),  '%3.1f°C %3.0f %%'%(temp,humi), font=font, fill=255)
    draw.text((0, top+16), '%3.0f hPa %3.0f 10kOhm'%(prea,vocR), font=font, fill=255)
    draw.text((0, top+25), str(zeit), font=font, fill=255)
    disp.image(image)
    disp.show()

    ### Erzeugt erstmalig eine Datenbank, wenn keine Vorhanden
    if not(os.path.isfile(dataDB)):
        sql = 'CREATE TABLE tabelle (zeit DATETIME UNIQUE, temp REAL, humi REAL, prea REAL, vocR REAL)'
        db = sqlite3.connect(dataDB)
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
        print('single-File-single-Table created')
    
    ## Einfügen Werte in die Datenbank
    sql = 'INSERT INTO tabelle (zeit, temp, humi, prea, vocR) VALUES (strftime("%Y-%m-%d %H:%M:%f", "' + str(zeit) + '"), %3.2f, %3.2f, %3.2f, %3.2f)'%(temp,humi,prea,vocR)
    db = sqlite3.connect(dataDB)
    cur = db.cursor()
    db.execute(sql)
    db.commit()
    cur.close()
    db.close()   
    print('%s | %3.1f °C | %3.1f %% | %3.1f hPa | %3.1f voc'%(zeit, temp, humi, prea, vocR))
    time.sleep(5)

