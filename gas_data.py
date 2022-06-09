# author: Minh
# date: June 09 2022
# To fetch gas price in major cities in Greater Vancouver, as well as major cities and provinces in Canada from GasBuddy

import requests, bs4, smtplib, datetime
import pandas as pd

def get_city_url(city): # function to get price list as raw text based on city
    url=f'http://www.vancouvergasprices.com/GasPriceSearch.aspx?typ=adv&fuel=A&srch=0&area={city}&site=Vancouver&station=All%20Stations&tme_limit=4'
    mozilla={'user-agent': 'Mozilla/5.0'}
    req=requests.get(url, headers=mozilla)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.content,'html.parser')
    text=''

    for index in range(10): # fetch top 10 gas price
        price_block=soup.find(id=f'rrlow_{index}').get_text()
        text=text+price_block
    return list(filter(None,text.split('\n')))

def get_city_price(get_url_city, city): # function to refine raw city price list text as table text
    price_list=[]
    company_list=[]
    address_list=[]

    for line in get_url_city:
        if ' ago' not in line and line != city and line != ' ':
            if 'update' in line:
                line=line.strip('update')
                price_list.append(line)
            elif len(line) < 13:
                company_list.append(line)
            else:
                address_list.append(line)

    df=pd.DataFrame({'Date': datetime.date.today(), 'Price': price_list, 'Station': company_list,f'{city} address': address_list})
    df.index=df.index + 1
    return df

def get_metro_url(): # function to get price list major cities as raw text
    url='http://www.vancouvergasprices.com/Prices_Nationally.aspx?d=metro'
    mozilla={'user-agent': 'Mozilla/5.0'}
    req=requests.get(url, headers=mozilla)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.content,'html.parser')
    raw_text=soup.find(id='list').get_text()
    raw_list=list(filter(None,raw_text.split('\n')))
    return raw_list[3:]

def get_metro_price(raw_metro): # function to refine raw major cities price list text as table text
    metro_list=[]
    price_list=[]

    for value in raw_metro:
        if value[0].isalpha():
            metro_list.append(value)
        else:
            price_list.append(value)
    
    df=pd.DataFrame({'Date': datetime.date.today(), 'Avg. Price': price_list, 'City': metro_list})
    df.index=df.index + 1
    return df

def get_area_url(): # function to get area price list as raw text
    url='http://www.vancouvergasprices.com/Prices_Nationally.aspx'
    mozilla={'user-agent': 'Mozilla/5.0'}
    req=requests.get(url, headers=mozilla)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.content,'html.parser')
    raw_text=soup.find(id='list').get_text()
    raw_list=list(filter(None,raw_text.split('\n')))
    return raw_list[3:]

def get_area_price(raw_area): # function to refine raw area price list text as table text
    area_list=[]
    price_list=[]

    for value in raw_area:
        if value[0].isalpha():
            area_list.append(value)
        else:
            price_list.append(value)
    
    df=pd.DataFrame({'Date': datetime.date.today(), 'Avg. Price': price_list, 'Area': area_list})
    df.index=df.index + 1
    return df

def email(gas_price, sender_email, bcc_email, password): # function to send email to desired address
    email_content='\r\n'.join([
    'From: Vegan Coder',
    f'BCC: {bcc_email}',
    f'Subject: Vancouver Gas Price Update on {datetime.date.today()}',
    '',
    f'{gas_price}'
    ])

    try:
        server=smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email,password)
        server.sendmail(sender_email, bcc_email, email_content)
        server.close()
    except:
        print('Something went wrong...')