import warnings
warnings.filterwarnings("ignore")

import pandas as pd 
import numpy as np 

from env import get_db_url

import os 

def get_logs_data():
    filename = 'logs_data.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col = 0)
    else:
        df = pd.read_sql(
        '''
        SELECT *
        FROM logs
        '''
        ,
        get_db_url('curriculum_logs')
        )
        
        df.to_csv(filename)
        
        return df




def get_cohorts_data():
    filename = 'cohorts_data.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col = 0)
    else:
        df = pd.read_sql(
        '''
        SELECT *
        FROM cohorts
        '''
        ,
        get_db_url('curriculum_logs')
        )
        
        df.to_csv(filename)
        
        return df