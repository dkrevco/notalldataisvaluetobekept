import pandas as pd
import re
import datetime
import qgrid
from collections import defaultdict
import httplib2
from googleapiclient import errors
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
import requests
from bs4 import BeautifulSoup
from dateutil import relativedelta
import csv
from oauth import authorize_creds, execute_request
import json



end_date = datetime.date.today()
start_date = end_date - relativedelta.relativedelta(months=3)

request = {
    'startDate': datetime.datetime.strftime(start_date, "%Y-%m-%d"),
    'endDate': datetime.datetime.strftime(end_date, "%Y-%m-%d"),
    'dimensions': ['page', 'query'],
    'rowLimit': 25000
    }

device_category = input('Enter device category: MOBILE, DESKTOP or TABLET: ').strip()

if device_category:
    request['dimensionFilterGroups'] = [{'filters':[{'dimension': 'device', 'expression': device_category}]}]

creds = 'auth/client_secrets.json'

site = 'https://www.iport.ru/'

webmasters_service = authorize_creds(creds)

response = execute_request(webmasters_service, site, request)

scDict = defaultdict(list)

for row in response['rows']:
    scDict['page'].append(row['keys'][0] or 0)
    scDict['query'].append(row['keys'][1] or 0)
    scDict['clicks'].append(row['clicks'] or 0)
    scDict['ctr'].append(row['ctr'] or 0)
    scDict['impressions'].append(row['impressions'] or 0)
    scDict['position'].append(row['position'] or 0)

with open('csv/test.txt', 'w', encoding='utf-8') as file:
    file.write(json.dumps(scDict))
    file.close()

df = pd.DataFrame(data = scDict)

df['clicks'] = df['clicks'].astype('int')
df['ctr'] = df['ctr'] * 100
df['impressions'] = df['impressions'].astype('int')
df['position'] = df['position'].round(2)
df.sort_values('clicks', inplace=True, ascending=False)

serp_results = 10

branded_queries = 'порт|port|gjhn|зщке'

df_cannibalized = df[df['position'] < serp_results]
df_cannibalized = df_cannibalized[~df_cannibalized['query'].str.contains(branded_queries, regex=True)]
df_cannibalized = df_cannibalized[df_cannibalized.duplicated(subset=['query'], keep=False)]
df_cannibalized.set_index(['query'], inplace=True)
df_cannibalized.sort_index(inplace=True)
df_cannibalized.reset_index(inplace=True)

df_cannibalized.to_csv('csv/df_cannibalized.csv', encoding='utf-8', index=False)

# def get_meta(url):
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     title = soup.find('title').get_text()
#     meta = soup.select('meta[name="description"]')[0].attrs["content"]
#     return title, meta
#
# df_cannibalized['title'], df_cannibalized['meta'] = zip(*df_cannibalized['page'].apply(get_meta))
# df_cannibalized

#
