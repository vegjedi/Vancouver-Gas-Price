# author: Minh
# date: May 27 2022
# To fetch gas price in Richmond, BC, Canada

import requests, bs4, smtplib
import pandas as pd

url='http://www.vancouvergasprices.com/GasPriceSearch.aspx?typ=adv&fuel=A&srch=0&area=Richmond&site=Vancouver&station=All%20Stations&tme_limit=12'
mozilla={'user-agent': 'Mozilla/5.0'}
req=requests.get(url, headers=mozilla)
req.raise_for_status()

soup=bs4.BeautifulSoup(req.content,'lxml')

text=''

for index in range(10): # fetch top 10 gas price
    price_block=soup.find(id=f'rrlow_{index}').get_text()
    text=text+price_block

text_list=text.split('\n')

price_list=[]
company_list=[]
address_list=[]

for line in text_list:
    if line != '' and line !=' ' and ' ago' not in line and 'Richmond' not in line:
        if 'update' in line:
            line=line.strip('update')
            price_list.append(line)
        elif len(line) < 13:
            company_list.append(line)
        else:
            address_list.append(line)

df=pd.DataFrame(list(zip(price_list, company_list, address_list)),columns =['Price', 'Company','Address'])
df.index = df.index + 1
daily_price=df.to_string()

email_content='\r\n'.join([
  'From: sender@gmail.com',
  'To: receiver@gmail.com',
  'Subject: Richmond Daily Gas Update',
  '',
  daily_price
  ])

try:
    server=smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sender@gmail.com','Password')
    server.sendmail('sender@gmail.com','receiver@gmail.com', email_content)
    server.close()
except:
    print('Something went wrong...')