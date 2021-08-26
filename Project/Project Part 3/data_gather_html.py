#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import sys
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


from urllib.request import urlopen
from bs4 import BeautifulSoup


# In[3]:


url = "http://rbi.ddns.net/getStopEvents"
html = urlopen(url)


# In[4]:


soup = BeautifulSoup(html, 'lxml')
h3 = soup.find_all('h3')


# In[5]:


trip_id_h3 =[]

for i in h3:
    str_h3 = str(i)
    cleantext = BeautifulSoup(str_h3, "lxml").get_text()
    trip_id_h3.append(cleantext)
    
global trip_id
trip_id = []
for i in trip_id_h3:
    x  = i.split(" ")
    #print(x)
    trip_id_num =  int(x[4])
    trip_id.append(trip_id_num)
#print(trip_id)


# In[6]:


tables = soup.find_all('table')
#print(len(tables))
flag = 0
stop_event = []

for table in tables:
    trip = trip_id[0]
    trip_id = trip_id[1:]
    
    rows = table.find_all('tr')
    #print(len(rows))
    if(flag == 0):
        row_th = rows[0].find_all('th')
        str_cells = str(row_th)
        header = BeautifulSoup(str_cells, "lxml").get_text()
        flag = 1

    for row in rows[1:]:
        row_td = row.find_all('td')
        str_cells1 = str(row_td)
        cleantext = BeautifulSoup(str_cells1, "lxml").get_text()
        
        # create a list from cleantext
        stop_event_rows = cleantext.split(", ")
        
        # strip "[" from first element of the list and "]" from the last element of the list
        x = stop_event_rows[0].split("[")
        stop_event_rows[0] = x[1]
        
        size = len(stop_event_rows)
        x = stop_event_rows[size-1].split("]")
        stop_event_rows[size-1] = x[0]
        
        for _ in range(len(stop_event_rows)):
            data = {}
            data["trip_id"] = trip
            data["vehicle_number"] = stop_event_rows[0]
            data["leave_time"] = stop_event_rows[1]
            data["train"] = stop_event_rows[2]            
            data["route_number"] = stop_event_rows[3]
            data["direction"] = stop_event_rows[4]
            data["service_key"] = stop_event_rows[5]
            data["stop_time"] = stop_event_rows[6]
            data["arrive_time"] = stop_event_rows[7]
            data["dwell"] = stop_event_rows[8]            
            data["location_id"] = stop_event_rows[9]
            data["door"] = stop_event_rows[10] 
            data["lift"] = stop_event_rows[11]
            data["ons"] = stop_event_rows[12]
            data["offs"] = stop_event_rows[13]           
            data["estimated_load"] = stop_event_rows[14]
            data["maximum_speed"] = stop_event_rows[15] 
            data["train_mileage"] = stop_event_rows[16]
            data["pattern_distance"] = stop_event_rows[17]
            data["location_distance"] = stop_event_rows[18]
            data["x_coordinate"] = stop_event_rows[19]            
            data["y_coordinate"] = stop_event_rows[20]
            data["data_source"] = stop_event_rows[21] 
            data["schedule_status"] = stop_event_rows[22] 
            
            #trip_id = trip_id[1:]
            json_str = json.dumps(data)
            data = json.loads(json_str)
            stop_event.append(data)

with open('test.json', 'w') as file:
    json.dump(stop_event, file, indent =2)    

sys.exit()


# In[ ]:




