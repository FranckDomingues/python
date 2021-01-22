# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:02:15 2018

@author: Utilizador Francisco Domingues
"""

import fitbit
import gather_keys_oauth2 as Oauth2
import numpy as np
import pandas as pd 
import datetime
import requests as req


CLIENT_ID = '22D8D6'
CLIENT_SECRET = '29b3078935f44634ff096c209304be84'


"""for obtaining Access-token and Refresh-token"""

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
 
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

 
"""Authorization"""
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

yesterday = str((datetime.datetime.now() - datetime.timedelta(days=5)).strftime ("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=5)).strftime ("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime ("%Y%m%d"))
today2 = str(datetime.datetime.now().strftime ("%Y-%m-%d"))


#get heart rate data / should be today
fitbit_stats2 = auth2_client.intraday_time_series('activities/heart', base_date=today2, detail_level='1sec')
stats2 = fitbit_stats2

time_list = []
val_list = []

for i in stats2['activities-heart-intraday']['dataset']:
    val_list.append(i['value'])
    time_list.append(i['time'])

heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})

#heartdf.to_csv('/Users/Utilizador/Desktop/SLEEPTRAINNER/HealthData/Heart/heart'+today+'.csv', columns=['Time','Heart Rate'], header=True, index = False)
heartdf.to_csv('./heart'+today+'.csv', columns=['Time','Heart Rate'], header=True, index = False)

#get heart summary
hsummarydf = pd.DataFrame({'Date':stats2["activities-heart"][0]['dateTime'],
                    'HR max':stats2["activities-heart"][0]['value']['heartRateZones'][0]['max'],
                    'HR min':stats2["activities-heart"][0]['value']['heartRateZones'][0]['min']},index=[0])
#hsummarydf.to_csv( /SLEEPTRAINNER/HealthData/heartsummary.csv', header=False, index=False, mode = 'a')
hsummarydf.to_csv('./heartsummary.csv', header=False, index=False, mode = 'a')

#get sleep summary
fitbit_stats2 = auth2_client.sleep(date='today')['sleep'][0]
ssummarydf = pd.DataFrame({'Date':fitbit_stats2['dateOfSleep'],
                         'MainSleep':fitbit_stats2['isMainSleep'],
                         'Efficiency':fitbit_stats2['efficiency'],
                         'Duration':fitbit_stats2['duration'],
                         'Minutes Asleep':fitbit_stats2['minutesAsleep'],
                         'Minutes Awake':fitbit_stats2['minutesAwake'],
                         'Awakenings':fitbit_stats2['awakeCount'],
                         'Restless Count':fitbit_stats2['restlessCount'],
                         'Restless Duration':fitbit_stats2['restlessDuration'],
                         'Time in Bed':fitbit_stats2['timeInBed']
                        },index=[0])
#ssummarydf.to_csv('/Users/Utilizador/Desktop/SLEEPTRAINNER/HealthData/sleepsummary.csv', header=False, index=False, mode = 'a')
ssummarydf.to_csv('./sleepsummary.csv', header=False, index=False, mode = 'a')

#get sleep data / should be today
fitbit_stats3 = auth2_client.sleep(date='today')
stime_list = []
sval_list = []

for i in fitbit_stats3['sleep'][0]['minuteData']:
    stime_list.append(i['dateTime'])
    sval_list.append(i['value'])
sleepdf = pd.DataFrame({'State':sval_list,
                     'Time':stime_list})
sleepdf['Interpreted'] = sleepdf['State'].map({'2':'Awake','3':'Very Awake','1':'Asleep'})
#sleepdf.to_csv('/Users/Utilizador/Desktop/SLEEPTRAINNER/HealthData/Sleep/sleep'+today+'.csv', columns = ['Time','State','Interpreted'], header=True, index = False)
sleepdf.to_csv('./sleep'+today+'.csv', columns = ['Time','State','Interpreted'], header=True, index = False)

sleep_data_to_send=fitbit_stats3['summary']
sleep_data_to_send['date']=fitbit_stats3['sleep'][0]['startTime']

hearts_data_to_send=dict() #send data information
hearts_data_to_send['heartZones']=stats2['activities-heart'][0]['value']['heartRateZones']
hearts_data_to_send['date']=stats2['activities-heart'][0]['dateTime']

#print(stats2)
#print(hearts_data_to_send)
print(sleep_data_to_send)
print(fitbit_stats3)

r = req.post('http://localhost:8081/heart',json=hearts_data_to_send)
r = req.post('http://localhost:8081/sleep',json=sleep_data_to_send)
r = req.post('http://localhost:8081/sleep',json=fitbit_stats3)
