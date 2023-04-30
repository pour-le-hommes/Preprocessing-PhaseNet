#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os
import obspy as obs
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from obspy import Trace
from obspy import Stream
from obspy.core import UTCDateTime
import shutil


# In[11]:


def tracedata(stream,div):
    
    if stream[0].id[3:7] != stream[1].id[3:7] and stream[0].id[3:7] != stream[2].id[3:7]:
        raise Exception('Not the same station')
        
    trace = stream[0].copy()
    sr = trace.stats.sampling_rate
    start_time = trace.stats.starttime
    end_time = trace.stats.endtime
    data_leng = len(trace.data)
    
    timegaps = (end_time-start_time)
    diff = (timegaps*sr-data_leng)/40
    window = int(timegaps)//div
    inter_time = start_time+window+diff+1
    
#     if ((inter_time-start_time)-window) != 0:
#         raise Exception(f'Data Window Mismatch {int(inter_time-start_time-diff)} != {window}')
        
    shift = window//2
    iterations = int(((timegaps-window)/shift)-1)
    
    return start_time,inter_time,shift,diff,iterations


# # Directory Paths

# In[246]:


fileraw = '1.Raw\\'
filesingle = '2.Singlecomp\\'
filethree = '3.Threecomp\\'
filedivided = '4.Pembagian\\'
fileresults = '5.Results\\'


# In[208]:


jawastationfile = 'nama_stasiun_jawa.csv'


# In[380]:


for i in range(len(os.listdir())):
    if os.listdir()[i][0:12]=='Data_Stasiun':
        stationfile = os.listdir()[i]


# ## Input Directory

# In[373]:


rawdatainput = input('Please give me the link to the raw data directory! \n')
rawdata = fr"{rawdatainput}\\"
# rawdata = r"C:\Users\bimoi\Documents\Coding\Jupyter_Notebook\TA\TA_Data\2020-08-17\\"
forcodeinput = input("I also need this code's directory to create the phasenet code! \n")
filedir = fr"{forcodeinput}\\"
# filedir = r'C:\Users\bimoi\Documents\Coding\Jupyter_Notebook\TA\Full_Automation\\'


# # CSV Files

# In[286]:


jawasta = pd.read_csv(jawastationfile)
datasta = pd.read_csv(stationfile)


# In[319]:


datasta.drop_duplicates(subset=['sta','phase'], inplace=True)


# # Make The Directories

# In[321]:


try:
    os.mkdir(fileraw)
except:
  print("Raw file already created")
try:
    os.mkdir(filesingle)
except:
  print("Single component file already created")
try:
    os.mkdir(filethree)
except:
  print("Three component file already created")
try:
    os.mkdir(filedivided)
except:
  print("Divided file already created")
try:
    os.mkdir(fileresults)
except:
  print("Results file already created")


# # Basic Datas

# In[322]:


BMKGstations = datasta.sta.to_list()
TimeBMKGStations = datasta.time.to_list()
PhaseBMKGStations = datasta.phase.to_list()
Javastations = jawasta.stasiun.to_list()
time = stationfile[13:23]


# ## Time Convertions of BMKG Stations

# In[323]:


ConvertedTimeBMKGStations = []
for i in range(len(TimeBMKGStations)):
    ConvertedTimeBMKGStations.append(UTCDateTime(f"{time}T{TimeBMKGStations[i]}"))


# # Comparing Jawa Station and BMKG Station Data

# In[324]:


BMKGStationComparison = list(dict.fromkeys(BMKGstations))


# In[387]:


Stations = []
notused = []
for i in tqdm(range(len(Javastations))):
    for j in range(len(BMKGStationComparison)):
        if BMKGStationComparison[j]==Javastations[i]:
            Stations.append(BMKGStationComparison[j])
print(f'A total of {len(Stations)} stations are used, {len(BMKGStationComparison)-len(Stations)} is found not to be a Java station')


# # Take Raw Data

# In[326]:


comps = os.listdir(rawdata)
if 'E' in comps and 'N' in comps and 'Z' in comps:
    pass
else:
    raise Exception('Not all component is found, the folders must be E,N,Z')


for i in range(len(comps)):
    stationtemp = Stations.copy()
    component = f"{comps[i]}"
    filedirraw = fr'{rawdata}\{component}'
    for j in tqdm(range(len(os.listdir(filedirraw)))):
        for k in range(len(stationtemp)):
            if stationtemp[k]== os.listdir(filedirraw)[j][3:7]:
                rawfilename = os.listdir(filedirraw)[j]
                rawfile = f"{filedirraw}\{rawfilename}"
                copyrawfile = f'{fileraw}\{rawfilename}'
                shutil.copyfile(rawfile, copyrawfile)
                stationtemp.remove(stationtemp[k])
                break
            
        if len(stationtemp)==0:
            break

print(f'A total of {len(Stations)-len(stationtemp)} stations are used, {len(stationtemp)} are not found in the raw data file')
print('The data has been filtered, copied, and saved in the Raw folder')


# # Converting Format To .SAC File

# In[327]:


print('Please open Seisgram2K to manually filter the data from the Raw folder')


# In[328]:


continueinput = input("Now convert it to .SAC and save it in the Singlecomp folder, press y when it's done! \n")
if continueinput=='y':
    pass
else:
    raise Exception("Yo, look what you did, now you have to start all over again")


# # Creating .MSEED File

# In[329]:


singlesacstream = Stream()
singlesacstream +=obs.read(f'{filesingle}\\*.sac',format='SAC')


# In[383]:


files = []
print("Changing and combining .SAC file to .MSEED file")
for i in tqdm(range(int(len(singlesacstream)/3))):
    if singlesacstream[0].id[3:7] == singlesacstream[1].id[3:7] and singlesacstream[0].id[3:7] == singlesacstream[2].id[3:7]:
        file = str('\\'+(singlesacstream[i*3].id[0:-1]))
        filename = file+".mseed"
        files.append(filename)
        singlesacstream[3*i:(3*i)+3].write(filethree+filename,format='mseed')
    else:
        raise Exception(f"Error!, file {singlesacstream[0].id[3:7]} doesn't have all the components")
    
print("Data have been preprocessed and put in the Threecomp folder")


# # Theecomp Stream File

# In[418]:


Threecomp = obs.read(f'{filethree}\*.mseed',format='MSEED')


# # Filtering BMKG Correction File

# In[433]:


Timestations = ConvertedTimeBMKGStations.copy()
Station = BMKGstations.copy()
tempcorrectionstation = BMKGstations.copy()
CorrectionPhaseBMKG = PhaseBMKGStations.copy()

for i in range(len(Threecomp)):
    for j in range(len(tempcorrectionstation)):
        if Threecomp[i].stats.station == tempcorrectionstation[j]:
            tempcorrectionstation[j]='used'

BMKGFile = pd.DataFrame()
BMKGFile['Station'] = Station
BMKGFile['Time_Station'] = Timestations
BMKGFile['Phase'] = CorrectionPhaseBMKG
BMKGFile['Usedfile'] = tempcorrectionstation


# # Saving Correction File

# In[434]:


BMKGFile = BMKGFile[BMKGFile.Usedfile == 'used']
BMKGFile = BMKGFile.drop(['Usedfile'],axis=1)
BMKGFile.to_csv(fileresults+'BMKGCorrectionfile.csv')


# # Time Trimming

# In[335]:


timestart = []
timeend = []
for i in range(len(Timestations)):
    timestart.append(Timestations[i]-(1*60))
    timeend.append(Timestations[i]+(4*60))


# In[336]:


Trimmedthreecomp = Threecomp.copy()
for i in range(len(Trimmedthreecomp)//3):
    for j in range(len(Stations)):
        if Trimmedthreecomp[i*3].stats.station==Stations[j]:
            Trimmedthreecomp.trim(timestart[i],timeend[i])


# # Resampling To 100 Hz

# In[236]:


Completethreecomp = Trimmedthreecomp.resample(100)


# # Save Complete Three Component File

# In[239]:


for i in tqdm(range(len(Completethreecomp)//3)):
    filename = str(Completethreecomp[i*3].id[0:-1])+'.mseed'
    print(Completethreecomp[i*3:(i*3)+3])
    Completethreecomp[i*3:(i*3)+3].write(filedivided+'\\'+filename,format='mseed')


# # Create Fname File

# In[240]:


filename = []
filetext = "Fnamefile.txt"
f= open(filetext,"w+")
print("Creating .txt file for csv format.")
f.write("fname\n")
for i in tqdm(range(len(os.listdir(filedivided)))):
        f.write(os.listdir(filedivided)[i]+"\n")
        filename.append(os.listdir(filedivided)[i])
f.close()


# # Create Code File

# In[244]:


filecode = "CodeFile.txt"
f= open(filecode,"w+")
print("Creating .txt file for the code.")
f.write(f"python phasenet/predict.py --model=model/190703-214543 --data_list={filedir}{filetext} --data_dir={filedir}{filedivided} --format=mseed --min_p_prob=0.6 --min_s_prob=0.6 --plot_figure")
f.close()


# # Full Report Print-out

# In[432]:


print('='*50)
print('FULL REPORT')
print('-'*20)
print(f'{len(BMKGStationComparison)} stations are from BMKG')
print(f'Of the {len(BMKGStationComparison)} stations from BMKG, {len(Stations)} are from Java')
print(f'And of the {len(Stations)} stations in Java, only {len(Stations)-len(stationtemp)} is found in the raw data with the directory you sent')
print(f"You've also filtered {len(Stations)-(len(threecomp)//3)} stations, which is great /s")

print(f'\nAll and all, from the BMKG station data to the results, it is {((len(Threecomp)//3)/len(BMKGStationComparison))*100}% of the data')

print(f'\nThe date of the event is {Timestations[0].date.isoformat()}')
print(f'The time of the event is around {Timestations[0].time.isoformat()} according to BMKG')
print('='*50)

