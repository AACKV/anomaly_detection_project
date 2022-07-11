import requests
import os
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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
            
    result_df = pd.concat([result_df,pd.DataFrame(locations)])
    result_df = result_df.drop_duplicates()
    
    result_df.to_csv(filename)

    return result_df

def webdev_visuals(wd_after_grad):
    wd_results = {'topic': ['javascript', 'java', 'css', 'spring', 'sql', 'jquery', 'appendix', 'capstone', 'random/ds_topics'], 
              'num_times_accessed': [wd_after_grad[wd_after_grad.path.str.contains('javascript[-/]|javascript$')].shape[0],
                                wd_after_grad[wd_after_grad.path.str.contains('java[-/]|_java|java$')].shape[0],
                                wd_after_grad[wd_after_grad.path.str.contains('css')].shape[0],
                                wd_after_grad[wd_after_grad.path.str.contains('spring')].shape[0],
                                wd_after_grad[wd_after_grad.path.str.contains('sql')].shape[0],
                                wd_after_grad[wd_after_grad.path.str.contains('jquery')].shape[0],
                                wd_after_grad[wd_after_grad.path.str.contains('appendix')].shape[0],
                                wd_after_grad[wd_after_grad.path.str.contains('capstone')].shape[0],
                                wd_after_grad.shape[0]- wd_after_grad[wd_after_grad.path.str.contains('java|sql|jquery|spring|css|appendix|capstone|toc')].shape[0]]}

    wd_results_df = pd.DataFrame(wd_results).sort_values('num_times_accessed', ascending=False)

    sns.barplot(data= wd_results_df, x = 'topic', y = 'num_times_accessed')
    plt.show()

    print("The two largest subgroups are as follows:\n"
     f"Java accounts for {round(wd_after_grad[wd_after_grad.path.str.contains('java[-/]|_java|java$')].shape[0] / wd_after_grad.shape[0], 4)*100}% \n"
     f"Javascript accounts for {round(wd_after_grad[wd_after_grad.path.str.contains('javascript[-/]|javascript$')].shape[0]/ wd_after_grad.shape[0], 4)*100}%")

def ds_visuals(ds_after_grad):
    ds_results = {'topic': ['capstone','sql','python', 'stats', 'fundamentals', 'regression', 'clustering', 'nlp', 'appendix', 'timeseries', 'anomaly', 'classification', 'spark', 'python', 'storytelling','other_topics'], 
              'num_times_accessed': [ds_after_grad[ds_after_grad.path.str.contains('capstone')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('sql')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('python')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('stats')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('fundamentals')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('regression')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('clustering')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('nlp')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('appendix')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('timeseries')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('anomaly')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('classification')].shape[0], 
                                ds_after_grad[ds_after_grad.path.str.contains('spark')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('python')].shape[0],
                                ds_after_grad[ds_after_grad.path.str.contains('storytelling')].shape[0],
                                ds_after_grad.shape[0]- ds_after_grad[ds_after_grad.path.str.contains('capstone|sql|python|stats|fundamentals|regression|clustering|nlp|appendix|timeseries|anomaly|classification|spark|python|storytelling')].shape[0]]}

    ds_results_df = pd.DataFrame(ds_results).sort_values('num_times_accessed', ascending=False)
    sns.barplot(data= ds_results_df, x = 'topic', y = 'num_times_accessed')
    plt.show()

    print("The two largest subgroups are as follows:\n"
     f"Java accounts for {round(ds_after_grad[ds_after_grad.path.str.contains('sql', case = False)].shape[0] / ds_after_grad.shape[0], 4)*100}% \n"
     f"Javascript accounts for {round(ds_after_grad[ds_after_grad.path.str.contains('fundamentals', case = False)].shape[0]/ ds_after_grad.shape[0], 4)*100}%\n"
     f"Classification accounts for {round(round(ds_after_grad[ds_after_grad.path.str.contains('classification', case = False)].shape[0]/ ds_after_grad.shape[0], 4)*100, 4)}%")
