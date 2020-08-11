from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.layouts import column
import numpy as np

import pandas as pd
import datetime as dt
import sqlite3


def chart(request):
    if request.POST: # wenn button gedrückt
        dic = request.POST # Werte von Page übernehmen
        print('mal sehen was das ist: ' + str(dic))
        nCycle = int(dic['nCycle'])
    else:
        nCycle = int(1)   
    chart = makeChart(nCycle)        
    return render(request, 'home.html', {'nCycle': nCycle, 'chart': chart})


#def makeChart(nCycle):
#    x = np.linspace(0,100,100)
#    y = np.sin(x/100*2*3.1415*nCycle)    
#    p1 = figure(plot_width=460, plot_height=200)
#    p1.line(x, y)
#    p1.toolbar.logo = None    
#    script, div = components(p1)
#    chart = script + div
#    return chart
 

def makeChart(nCycle):
    zeit = dt.datetime.now() - dt.timedelta(days=nCycle)
    zeit = zeit.strftime('%Y-%m-%d')
    db = sqlite3.connect('dataDB.sqlite3')
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
    ph = 300
    pw = 1000
     
    ## Temperatur ##
    p1 = figure(title='Temperatur', plot_width=pw, plot_height=ph, /
                x_axis_type='datetime', tooltips = tt, tools = werkzeuge)
    p1.line(x = 'zeit', y = 'temp', source = df, legend_label = 'Temperatur',  color='green')
    p1.xaxis.axis_label = 'Zeit'
    p1.legend.location = 'top_right'
    p1.legend.click_policy="hide" # Kurve ein/ausschaltbar
    p1.toolbar.logo = None
       
    ## Rel.Feuchte ##
    p2 = figure(title='Relative Feuchte', plot_width=pw, plot_height=ph, /
                x_axis_type='datetime', tooltips = tt, tools = werkzeuge)
    p2.line(x = 'zeit', y = 'humi', source = df, legend_label = 'Rel. Feuchte',  color='blue')
    p2.xaxis.axis_label = 'Zeit'
    p2.legend.location = 'top_right'
    p2.legend.click_policy="hide" # Kurve ein/ausschaltbar
    p2.toolbar.logo = None    
    p2.x_range = p1.x_range
    
    ## Luftdruck ##
    p3 = figure(title='Luftdruck', plot_width=pw, plot_height=ph, /
                x_axis_type='datetime', tooltips = tt, tools = werkzeuge)
    p3.line(x = 'zeit', y = 'prea', source = df, legend_label = 'Luftdruck',  color='blue')
    p3.xaxis.axis_label = 'Zeit'
    p3.legend.location = 'top_right'
    p3.legend.click_policy="hide" # Kurve ein/ausschaltbar
    p3.toolbar.logo = None    
    p3.x_range = p1.x_range
    
    ## VOC ##
    p4 = figure(title='VOC', plot_width=pw, plot_height=ph, x_axis_type='datetime', tooltips = tt, tools = werkzeuge)
    p4.line(x = 'zeit', y = 'vocR', source = df, legend_label = 'VOC',  color='blue')
    p4.xaxis.axis_label = 'Zeit'
    p4.legend.location = 'top_right'
    p4.legend.click_policy="hide" # Kurve ein/ausschaltbar
    p4.toolbar.logo = None    
    p4.x_range = p1.x_range
    
    allCharts = column(p1, p2, p3, p4) 
    script, div = components(allCharts)
    chart = script + div
    return chart
   

    