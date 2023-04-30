#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import obspy as obs
from datetime import datetime
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt


# In[2]:


def Preprodata(df):
    datetime = []
    for i in range(len(df.index)):
        datetime.append(pd.to_datetime(df.phase_time[i]))
    df['Time'] = datetime
#     df['date'] = [d.date() for d in df['phase_time']]
#     df['time'] = [d.time() for d in df['phase_time']]
    data = df[['station_id','phase_index','phase_score','phase_time','phase_type']].sort_values('phase_score')
    Pscore = data[data['phase_type']=="P"]
    Sscore = data[data['phase_type']=="S"]
    Pscore.reset_index(inplace=True, drop=True)
    Sscore.reset_index(inplace=True, drop=True)
    
    return data,Pscore,Sscore


# # Read CSV Files

# In[67]:


picks = pd.read_csv(r"5.Results\picks.csv")
correctionfile = pd.read_csv(r"5.Results\BMKGCorrectionfile.csv")


# # Data Formatting

# In[69]:


alldata,alldatapscore,alldatasscore = Preprodata(picks)


# In[70]:


datastanodup = correctionfile.copy()
datastanodup.drop_duplicates(inplace=True)


# In[71]:


Dateofevent = datastanodup.Time_Station[0][0:10]


# In[7]:


alldata.sort_values(['station_id'],inplace=True)
datastanodup.sort_values('Station',inplace=True)


# In[8]:


stationname = []
for i in range(len(alldata)):
    stationname.append(alldata.station_id[i][3:7])
alldata['station_name'] = stationname


# In[37]:


# Create New Data Set
arrbmkg = []
arrphase = []
wavetype = []
station = []
phase_score = []
phase_sta = []


# In[38]:


samesta = 0
for i in range(len(alldata)):
    for j in range(len(datastanodup)):
        if alldata.station_name[i]==datastanodup.Station[j]:
            samesta = samesta+1
            if alldata.phase_type[i]==datastanodup.Phase[j]:
                arrbmkg.append(datastanodup.Time_Station[j])
                station.append(datastanodup.Station[j])
                arrphase.append(alldata.phase_time[i])
                wavetype.append(alldata.phase_type[i])
                phase_sta.append(alldata.station_name[i])
                phase_score.append(alldata.phase_score[i])


# In[39]:


fulldata = pd.DataFrame()
fulldata['Station_Name'] = station
fulldata['Arrival_BMKG'] = arrbmkg
fulldata['Station_Name_PhaseNet'] = phase_sta
fulldata['Arrival_PhaseNet'] = arrphase
fulldata['Arrival_Phase'] = wavetype
fulldata['Phase_Score'] = phase_score


# In[66]:


fulldata


# In[40]:


time = fulldata.Arrival_PhaseNet.copy()


# In[41]:


timetransformedphase = []
for i in range(len(time)):
    timetransformedphase.append(UTCDateTime(time[i]))


# In[42]:


time = fulldata.Arrival_BMKG.copy()


# In[43]:


timetransformedbmkg = []
for i in range(len(time)):
    timetransformedbmkg.append(UTCDateTime(time[i]))


# In[44]:


timebmkg = timetransformedbmkg.copy()
timephase = timetransformedphase.copy()


# In[45]:


x = []
y = []
for i in range(len(timebmkg)):
    value = timebmkg[i]-timephase[i]
    x.append(i)
    y.append(value)


# In[47]:


bi = np.arange(np.min(y),np.max(y),5)
bi


# In[65]:


counts, bins = np.histogram(y,bins=bi)
plt.hist(bins[:-1], bins, weights=counts)
title = f'Perbedaan Picking Phasenet dan BMKG event {Dateofevent}'
plt.title(f'{title}')
plt.xlabel('Selisih waktu (s)')
plt.ylabel('Jumlah Kejadian')
plt.plot()

plt.savefig(fr"5.Results/{title}.jpg")


# In[ ]:




