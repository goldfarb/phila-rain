import csv
import os
import pandas as pd
import re
import requests
from io import StringIO
from twilio.rest import Client


a = requests.get('https://forecast.weather.gov/data/obhistory/KPHL.html')
b = a.text
c = re.sub(r'<!DOCTYPE HTML PUBLIC.*?<tr align="center" bgcolor="#b0c4de">','<tr>',b, flags=re.DOTALL)
d = re.sub(r'</tr><tr align="center" bgcolor="#b0c4de"><th rowspan="3">D<br>a<br>t<br>e</th>.*</tr></table></body></html>','</tr>', c, flags=re.DOTALL)
e = re.sub(r'</td><td>',',', d)
f = re.sub(r'</td>\s*<td>',',', e)
g = re.sub(r'</td><td align=".*?">',',', f)
h = re.sub(r'</td></tr><tr.*?><td>','\n', g)
i = re.sub(r'<tr><th rowspan=.*<td>','date,time,wind,vis,wx,sky,at,dwpt,max,min,hum,chill,heat,alt,sl,1hr,3hr,6hr\n',h,flags=re.DOTALL)
j = re.sub(r'</td></tr>','',i)
csv_string = StringIO(j)
df = pd.read_csv(csv_string, sep = ",")
s = df['6hr']
t = str(f'{s.sum():.2f}')
sms = "Happy birthday! It has rained " + t + " inches in the past three days."


account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body=sms,
         from_='+13262223190',
         to='+14134463861'
     )
