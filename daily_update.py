# author: Minh
# date: June 09 2022
# To archive data to csv and send email

from gas_data import *

city_list=['Richmond'] # insert which city in Greater Vancouver to get gas price
final_price_list=[]

for city in city_list: # extract content, save data and convert to text
    city_data=get_city_price(get_city_url(city),city)
    city_data.to_csv('./data/city_data.csv',mode='a', index=False, header=False)
    final_price_list.append(city_data.to_string())
      
metro_data=get_metro_price(get_metro_url())
metro_data.to_csv('./data/metro_data.csv',mode='a', index=False, header=False)
final_price_list.append(metro_data.to_string())

area_data=get_area_price(get_area_url())
area_data.to_csv('./data/area_data.csv',mode='a', index=False, header=False)
final_price_list.append(area_data.to_string())

gas_price='\n\n'.join(final_price_list)

email(gas_price, sender_email, bcc_email, sender_password)