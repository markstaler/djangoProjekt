# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:39:50 2020

@author: mark
"""

#from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.layouts import column
from bokeh.io import output_file, show
import numpy as np

import pandas as pd
import datetime as dt
import sqlite3




#zeit = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#temp=humi=prea=vocR=3.2
#sql = 'INSERT INTO tabelle (zeit, temp, humi, prea, vocR) VALUES (DATETIME("' + str(zeit) + '"), %3.2f, %3.2f, %3.2f, %3.2f)'%(temp,humi,prea,vocR)
#print(sql)







zeit = dt.datetime.now() - dt.timedelta(days=1)
zeit = zeit.strftime('%Y-%m-%d')
db = sqlite3.connect('messDB.sqlite3')
df = pd.read_sql_query('SELECT * FROM tabelle WHERE zeit>strftime("%Y-%m-%d","'+zeit+'")', db)
df = pd.read_sql_query('SELECT * FROM tabelle', db)
db.close() 

df['zeit'] = pd.to_datetime(df['zeit'])
tStr = [] # Zeit als String um später mit Tool Tip anzeigen zu können
for i in df['zeit']:
    tStr.append(i.strftime('%Y-%m-%d %H:%M:%S'))
df['tStr'] = tStr


werkzeuge =  "pan, box_zoom, reset, save, hover"
tt = [('Zeit:','@tStr'), ('y:', '$y')]
ph = 400
pw = 1400
 
## Temperatur ##
p1 = figure(title='Temperatur', plot_width=pw, plot_height=ph, x_axis_type='datetime', tooltips = tt, tools = werkzeuge)
p1.line(x = 'zeit', y = 'temp', source = df, legend_label = 'Temperatur',  color='green')
p1.xaxis.axis_label = 'Zeit'
p1.legend.location = 'top_right'
p1.legend.click_policy="hide" # Kurve ein/ausschaltbar
p1.toolbar.logo = None
   
## Rel.Feuchte ##
p2 = figure(title='Relative Feuchte', plot_width=pw, plot_height=ph, x_axis_type='datetime', tooltips = tt, tools = werkzeuge)
p2.line(x = 'zeit', y = 'humi', source = df, legend_label = 'Rel. Feuchte',  color='blue')
p2.xaxis.axis_label = 'Zeit'
p2.legend.location = 'top_right'
p2.legend.click_policy="hide" # Kurve ein/ausschaltbar
p2.toolbar.logo = None    
p2.x_range = p1.x_range

allCharts = column(p1, p2) 
script, div = components(allCharts)
chart = script + div
show(allCharts)
