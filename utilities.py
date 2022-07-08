import requests
import os
import pandas as pd 
import numpy as np

def scrape_ip_locations(df, index_num=0):
    """ needs original log df (900000 rows), index_num = n where n is which ip address index you want to start at."""
    locations = []
    i=0
    
    filename = 'ip_geographical_data.csv'
    
    if os.path.isfile(filename):
        result_df = pd.read_csv(filename)
    else:
        result_df = pd.DataFrame()
    
    # add bracket after 'ip_list' with number to add to df
    # 684
    
    ip_list = df.ip.unique()[index_num:]
    for ip in ip_list:
        url = f'http://ipinfo.io/{ip}/json'
        data = requests.get(url).json()

        i+=1
        print(f'\r{i}', end='')
        try:
            IP=data['ip']
            org=data['org']
            city = data['city']
            country=data['country']
            region=data['region']
            locations.append({'ip':IP, 'org':org, 'city':city, 'country':country, 'region':region})
        except:
            print(data)
            
    result_df = pd.concat([result_df,locations])
    result_df = result_df.drop_duplicates()
    
    result_df.to_csv(filename)

    return result_df