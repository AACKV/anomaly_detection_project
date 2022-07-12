import warnings
warnings.filterwarnings("ignore")

import pandas as pd 
import numpy as np 

from env import get_db_url

import os 

def get_logs_data():
    ''' This function reads in the logs data from the curriculum_logs Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
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

    ''' This function reads in the logs data from the curriculum_logs Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''

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



def wrangle_logs():
    '''Wrangles the curriculum access logs, converts date + time to one datetime column, drops unnecessary columns'''
    
    # load in cohort/logs
    cohorts = get_cohorts_data()
    logs = get_logs_data()

    # dropping unnamed col
    for col in cohorts.columns:
        if 'Unnamed' in col or 'deleted' in col:
            cohorts = cohorts.drop(columns=[col])

    for col in logs.columns:
        if 'Unnamed' in col:
            logs = logs.drop(columns=[col])

    # Join and format final table
    logs = logs.fillna(0)
    df = pd.merge(left_on=logs.cohort_id, right_on=cohorts.id, left=logs, right=cohorts,how='outer')
    df.date = pd.to_datetime(df.date + " " + df.time)
    df = df.drop(columns=['key_0', 'id', 'time'])

    return df

def make_datetime_index(df):
    df = df.set_index('date').sort_index()
    return df