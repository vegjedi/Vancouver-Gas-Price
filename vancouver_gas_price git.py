# author: Minh
# date: May 30 2022
# To fetch gas price in major cities in Greater Vancouver, Canada from GasBuddy

import requests, bs4, smtplib
import pandas as pd

target_city=['Richmond', 'Vancouver','Burnaby', 'Surrey', 'Langley']

def get_url(city): # function to get price list as raw text based on city
    url=f'http://www.vancouvergasprices.com/GasPriceSearch.aspx?typ=adv&fuel=A&srch=0&area={city}&site=Vancouver&station=All%20Stations&tme_limit=4'
    mozilla={'user-agent': 'Mozilla/5.0'}
    req=requests.get(url, headers=mozilla)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.content,'html.parser')
    text=''

    for index in range(5): # fetch top 5 gas price
        price_block=soup.find(id=f'rrlow_{index}').get_text()
        text=text+price_block
    return list(filter(None,text.split('\n')))

def get_price(city): # function to refine raw price list text as table text
    price_list=[]
    company_list=[]
    address_list=[]

    for line in text_list:
        if ' ago' not in line and line != city and line != ' ':
            if 'update' in line:
                line=line.strip('update')
                price_list.append(line)
            elif len(line) < 13:
                company_list.append(line)
            else:
                address_list.append(line)

    df=pd.DataFrame(list(zip(price_list, company_list, address_list)),columns =['Price', 'Company',f'Address in {city}'])
    df.index=df.index + 1
    return df.to_string()

def email(gas_price, sender_email, receiver_email, password): # function to send email to desired address
    email_content='\r\n'.join([
    f'From: {sender_email}',
    f'To: {receiver_email}',
    'Subject: Vancouver Daily Gas Price Update',
    '',
    f'{gas_price}'
    ])

    try:
        server=smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(f'{sender_email}',f'{password}')
        server.sendmail(f'{sender_email}',f'{receiver_email}', email_content)
        server.close()
    except:
        print('Something went wrong...')

final_price_list=[]

for city in target_city: 
    text_list=get_url(city)
    final_price_list.append(get_price(city))

gas_price='\n\n'.join(final_price_list)

email(gas_price, 'sending_address@gmail.com', 'receiving_address@gmail.com', 'your_sending_password')