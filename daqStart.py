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
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
from threading import Thread
import comMod


#def startDjango(ip): # Funktion zum Start Django als separater Threat
##    cmd = ['vncserver', '-randr=1400x900'] # vorläufiger Fix zur Einstellung VNC Auflösung bei headless-Betrieb
##    subprocess.call(cmd)
#
#    directory = os.path.dirname(__file__)        
#    print(directory)
#    cmd = ['python3', '/home/pi/daqProjekt/manage.py', 'runserver', ip+':8000']
#    subprocess.call(cmd)
#
#messDB = '/home/pi/daqProjekt/messDB.sqlite3'

## Initalize Display
i2c = busio.I2C(SCL, SDA) # Create the I2C interface.
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c) # Create the SSD1306 OLED class. pixel width/height
width = disp.width
height = disp.height
image = Image.new('1', (width, height)) # Create blank image for drawing.
draw = ImageDraw.Draw(image) # Get drawing object to draw on image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
font = ImageFont.load_default() # Load default font.

#### Initialisierung BME680
#sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)    
#sensor.set_humidity_oversample(bme680.OS_2X)
#sensor.set_pressure_oversample(bme680.OS_4X)
#sensor.set_temperature_oversample(bme680.OS_8X)
#sensor.set_filter(bme680.FILTER_SIZE_3)
#sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
#sensor.set_gas_heater_temperature(320)
#sensor.set_gas_heater_duration(150)
#sensor.select_gas_heater_profile(0)

#for i in range(5):
#    time.sleep(5)
#    ## erfasse IP-Adresse vom Linuxsystem (nicht Windows)
#    ipAll = subprocess.check_output('hostname -I', shell=True).decode('utf-8')
#    ip = ipAll[0:ipAll.find(' ')]
#    
#    if len(ip)>6 and len(ip)<18: # wenn Netzwerk gefunden und IP bezogen
#        ## Starte Django-Entwicklungsserver als eigener Thread
#        t = Thread(target=startDjango, args=(ip,))
#        t.start()
#        print('Django started')
#        break
#
#while True:  
##for j in range(5):
#    
##   ##  Messen
#    zeit = dt.datetime.now()
#    
#    sensor.get_sensor_data()
#    temp = sensor.data.temperature
#    humi = sensor.data.humidity
#    prea = sensor.data.pressure
#    vocR = sensor.data.gas_resistance/10000 # 10kOhm = 10kOhm
#    data = comMod.comHukse('/dev/ttyAMA0')
#    hPyr = data['HPyr']
#    tPyr = data['TPyr']
#     
     
# Display
ipAll = subprocess.check_output('hostname -I', shell=True).decode('utf-8')
ip = ipAll[0:ipAll.find(' ')]
top = -2
draw.rectangle((0, 0, width, height), outline=0, fill=0) # Draw a black filled box to clear the image.
draw.text((0, top+0),ip+':8000' , font=font, fill=255)
#    draw.text((0, top+8),  '%3.1f°C %3.0f %%'%(temp,humi), font=font, fill=255)
#    draw.text((0, top+16), '%3.0f hPa %3.0f 10kOhm'%(prea,vocR), font=font, fill=255)
draw.text((0, top+25), str(zeit), font=font, fill=255)
disp.image(image)
disp.show()

#    ### Erzeugt erstmalig eine Datenbank, wenn keine Vorhanden
#    if not(os.path.isfile(messDB)):
#        sql = 'CREATE TABLE tabelle (zeit DATETIME UNIQUE, temp REAL, humi REAL, prea REAL, vocR REAL, hPyr REAL, tPyr REAL)'
#        db = sqlite3.connect(messDB)
#        cur = db.cursor()
#        cur.execute(sql)
#        db.commit()
#        cur.close()
#        db.close()
#        print('single-File-single-Table created')
#    
#    ## Einfügen Werte in die Datenbank
#    sql = 'INSERT INTO tabelle (zeit, temp, humi, prea, vocR, hPyr, tPyr) VALUES (DATETIME("' + str(zeit) + '"), %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f)'%(temp,humi,prea,vocR, hPyr, tPyr)
#    db = sqlite3.connect(messDB)
#    cur = db.cursor()
#    db.execute(sql)
#    db.commit()
#    cur.close()
#    db.close()   
#    print(sql)
#    time.sleep(3)

