import requests
import os
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.express as px
import wrangle

def scrape_ip_locations(df, index_num=0):
    '''
    Needs original access log df (900000 rows), index_num = n where n is which ip address index you want to start at
    if you don't want to scrape all at once. 
    '''
    
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
    '''
    This function takes in a dataframe of Web Development students' curriculum access logs post graduation and plots out a visual of 
    the data showing the most commonly accessed topics and prints out a statement giving percentage values of each of the two largest 
    topics.
    '''

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
    
    plt.figure(figsize=(16, 5))
    sns.barplot(data= wd_results_df, x = 'topic', y = 'num_times_accessed')
    plt.title('Web Development Curriculum Access Post Graduation')
    plt.show()

    print("The two largest topics are as follows:\n"
     f"Java accounts for {round(wd_after_grad[wd_after_grad.path.str.contains('java[-/]|_java|java$')].shape[0] / wd_after_grad.shape[0], 4)*100}% \n"
     f"Javascript accounts for {round(wd_after_grad[wd_after_grad.path.str.contains('javascript[-/]|javascript$')].shape[0]/ wd_after_grad.shape[0], 4)*100}%")

def ds_visuals(ds_after_grad):
    '''
    This function takes in a dataframe of Data Science students' curriculum access logs post graduation and plots out a visual of the 
    data showing the most commonly accessed topics and prints out a statement giving percentage values of each of the three largest 
    topics.
    '''
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

    plt.figure(figsize=(16, 5)) 
    ds_results_df = pd.DataFrame(ds_results).sort_values('num_times_accessed', ascending=False)
    sns.barplot(data= ds_results_df, x = 'topic', y = 'num_times_accessed')
    plt.title('Data Science Curriculum Access Post Graduation')
    plt.show()

    print("The largest topics are as follows:\n"
     f"SQL accounts for {round(ds_after_grad[ds_after_grad.path.str.contains('sql', case = False)].shape[0] / ds_after_grad.shape[0], 4)*100}% \n"
     f"Fundamentals accounts for {round(ds_after_grad[ds_after_grad.path.str.contains('fundamentals', case = False)].shape[0]/ ds_after_grad.shape[0], 4)*100}%\n"
     f"Classification accounts for {round(round(ds_after_grad[ds_after_grad.path.str.contains('classification', case = False)].shape[0]/ ds_after_grad.shape[0], 4)*100, 4)}%")

def webdev_subtopics():
    '''
    This function visually represents the most accessed single lessons/paths for Web Development graduates post graduation. It 
    specifically highlights how the top four results are all lessons covering Spring.
    '''

    # Making a dataframe to contain the most accessed subtopics
    sub_topics_list = ['java-i/introduction-to-java', 
                    'java-i/syntax-types-and-variables', 
                    'java-ii/object-oriented-programming', 
                    'java-iii/servlets', 
                    'javascript-i/functions', 
                    'javascript-i/javascript-with-html', 
                    'spring/fundamentals/controllers', 
                    'spring/setup', 
                    'spring/fundamentals/views',
                    'spring/fundamentals/repositories',
                    'html-css/elements',
                    'html-css/introduction']
    occurances_list = [894, 847, 822, 811, 785, 775, 1299, 1236, 1166, 1073, 937, 800]
    wd_subtopics = {'subtopic': sub_topics_list, 'num_times_accessed': occurances_list}
    wd_subtopics_df = pd.DataFrame(wd_subtopics).sort_values('num_times_accessed', ascending=False)

    plt.figure(figsize=(16, 5)) 
    clrs = ['#2BA823', '#2BA823', '#2BA823', '#2BA823', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey' ]
    sns.barplot(data= wd_subtopics_df, x = 'subtopic', y = 'num_times_accessed', palette = clrs)
    plt.title('Web Dev Curriculum Access Post Graduation - Specific subtopic')
    red_patch = mpatches.Patch(color='#2BA823', label='Lessons covering Spring')
    plt.legend(handles=[red_patch], fontsize=15)
    plt.xticks(rotation=65)
    plt.show()


def anomalies_df(df):
    '''this function takes in a dataframe and gets a count of anomalies by user.''' 

    def prep(df, user):
        '''this function takes the user and gets the count of the number of paths that a user takes by day'''

        df = df[df.user_id == user]
        pages = df['path'].resample('d').count()
        return pages

    def compute_pct_b(pages, span, weight, user):
        '''this function gets the bandwidth that was used in a day'''
        midband = pages.ewm(span=span).mean()
        stdev = pages.ewm(span=span).std()
        ub = midband + stdev*weight
        lb = midband - stdev*weight
        bb = pd.concat([ub, lb], axis=1)
        my_df = pd.concat([pages, midband, bb], axis=1)
        my_df.columns = ['pages', 'midband', 'ub', 'lb']
        my_df['pct_b'] = (my_df['pages'] - my_df['lb'])/(my_df['ub'] - my_df['lb'])
        my_df['user_id'] = user
        return my_df

    def plt_bands(my_df, user):
        '''this function plots the bandwidth used by day. the x represents time and the y represents the number of pages'''
        fig, ax = plt.subplots(figsize=(12,8))
        ax.plot(my_df.index, my_df.pages, label='Number of Pages, User: '+str(user))
        ax.plot(my_df.index, my_df.midband, label = 'EMA/midband')
        ax.plot(my_df.index, my_df.ub, label = 'Upper Band')
        ax.plot(my_df.index, my_df.lb, label = 'Lower Band')
        ax.legend(loc='best')
        ax.set_ylabel('Number of Pages')
        plt.show()

    def find_anomalies(df, user, span, weight):
        '''this function uses the compute_pct_b function and returns results where that where the result is greater than 1'''
        pages = prep(df, user)
        my_df = compute_pct_b(pages, span, weight, user)
        return my_df[my_df.pct_b>1]
    '''the following section establishes an anomaly df with the top 6 anomalies. These top 6 each had 150+ pages.'''
    user = 1
    span = 30
    weight = 6
    user_df = find_anomalies(df, user, span, weight)

    anomalies = pd.DataFrame()
    user_df = find_anomalies(df, user, span, weight)
    anomalies = pd.concat([anomalies, user_df], axis=0)

    span = 30
    weight = 3.5

    anomalies = pd.DataFrame()
    for u in list(df.user_id.unique()):
        user_df = find_anomalies(df, u, span, weight)
        anomalies = pd.concat([anomalies, user_df], axis=0)

    df = anomalies[anomalies.pages  >= 100]
    df = df.sort_values(by = ['pages'], ascending = False)

    columns = ['midband', 'ub', 'lb', 'pct_b']
    df = df.drop(columns, axis = 1)

    df = df.head(6)

    def anomaly_df_builder(df):
        '''this function adds ip, cohort, city, country, and region(state) of the user to the anomaly df'''
        suspicious_ips = ['204.44.112.76', '108.65.244.91', '172.124.70.146', '70.130.123.81', '99.88.62.179', '136.50.20.17']
        cohort_list = ['Zion', 'Teddy' , 'Europa' , 'Hyperion', 'Europa', 'Wrangell' ]
        city_list = ['Dallas', 'San_Antonio' , 'San_Antonio' , 'San_Antonio' , 'San_Antonio', 'San_Antonio']
        country_list = ['US','US','US','US','US', 'US']
        region_list = ['Texas','Texas','Texas','Texas', 'Texas', 'Texas']
        df = df.assign(cohort = cohort_list,
                                       ip = suspicious_ips,
                                       city = city_list, 
                                      country = country_list,
                                      region = region_list)
        return df

    df = anomaly_df_builder(df)
    return df

def pages_chart(df):
    '''this function creates an interactive chart that plots the number of pages visited per day'''
    pages = df['path'].resample('d').count()
    return px.line(x = pages.index, y = pages)



def accessed_once_series(df):
    '''
    Input is the original dataframe, returns a series of paths that were only accessed once.
    '''

    series = pd.Series((df.path.value_counts()==1).index, name='paths').dropna()
    return series

def least_accessed(the_df):
    '''
    Returns a df that contains the times a certain topic has been accessed by its appearance in a path.
    Topics defined by 'topics' list.
    '''

    df = accessed_once_series(the_df)

    topics = ['sql', 'python', 'stats', 'fundamentals', 'regression', 'clustering', 'nlp',
              'appendix', 'timeseries', 'anomaly', 'classification', 'spark', 'storytelling', 'javascript', 'java',
             'css', 'spring', 'jquery', 'capstone', 'php', 'cli', 'git', 'laravel', 'angular', 'web-design', 
             'prework', 'apache', 'django', 'other_topics', 'pre-work']

    all_topics_reg_ex = '|'.join(topics)
    results = {'topic': topics, 
                  'num_times_accessed': [df[df.str.contains('sql')].shape[0],
                                    df[df.str.contains('python')].shape[0],
                                    df[df.str.contains('stats')].shape[0],
                                    df[df.str.contains('fundamentals')].shape[0],
                                    df[df.str.contains('regression')].shape[0],
                                    df[df.str.contains('clustering')].shape[0],
                                    df[df.str.contains('nlp')].shape[0],
                                    df[df.str.contains('appendix')].shape[0],
                                    df[df.str.contains('timeseries')].shape[0],
                                    df[df.str.contains('anomaly')].shape[0],
                                    df[df.str.contains('classification')].shape[0], 
                                    df[df.str.contains('spark')].shape[0],
                                    df[df.str.contains('storytelling')].shape[0],
                                    df[df.str.contains('javascript[-/]|javascript$')].shape[0],
                                    df[df.str.contains('java[-/]|_java|java$')].shape[0],
                                    df[df.str.contains('css')].shape[0],
                                    df[df.str.contains('spring')].shape[0],
                                    df[df.str.contains('jquery')].shape[0],
                                    df[df.str.contains('capstone')].shape[0],
                                    df[df.str.contains('php')].shape[0],
                                    df[df.str.contains('cli')].shape[0],
                                    df[df.str.contains('git')].shape[0],
                                    df[df.str.contains('laravel')].shape[0],
                                    df[df.str.contains('angular')].shape[0],
                                    df[df.str.contains('web-design')].shape[0],
                                    df[df.str.contains('prework')].shape[0],
                                    df[df.str.contains('apache')].shape[0],
                                    df[df.str.contains('django')].shape[0],
                                    df.shape[0]- df[df.str.contains(all_topics_reg_ex)].shape[0],
                                    df[df.str.contains('pre-work')].shape[0]]}

    results = pd.DataFrame(results).sort_values('num_times_accessed', ascending=False)
    return results

def other_topics(df):
    ''' 
    Returns a series of the pages accessed once that don't fall into a specified category,
    categories being defined by the list 'topics'.
    '''

    series = accessed_once_series(df)
    
    topics = ['sql', 'python', 'stats', 'fundamentals', 'regression', 'clustering', 'nlp',
              'appendix', 'timeseries', 'anomaly', 'classification', 'spark', 'storytelling', 'javascript', 'java',
             'css', 'spring', 'jquery', 'capstone', 'php', 'cli', 'git', 'laravel', 'angular', 'web-design', 'prework',
             'apache', 'django', 'pre-work']

    all_topics_reg_ex = '|'.join(topics)
    
    series = series[~series.str.contains(all_topics_reg_ex, case=False)]
    
    return series

def without_file_pages(the_df):
    ''' 
    Returns a series of least viewed pages without file extensions at the end of a path.
    '''
    
    series = accessed_once_series(the_df)
    files = ['.html', '.json', '.aspx', '.jpg', '.jpeg', '.png', '.csv', '.mov', '.zip', 'slides', '.md', '.txt',
             '.ico']
    files = [file+ '$' if file != 'slides' else file for file in files]
    files = '|'.join(files)
    
    series = series[~series.str.contains(files)]
    
    return series


def create_least_viewed_viz(df):
    '''
    Creates the data for least accessed pages, then graphs the pages
    categorized by subtopic. Takes in the original data frame.
    '''

    df.path = df.path.astype('string')
    df= df.fillna(' ')
    least= least_accessed(df)

    plt.title('Subject Frequency in Least Viewed Pages')
    sns.barplot(data= least[:6], x = 'topic', y = 'num_times_accessed')
    
def no_cohorts():
    altdf = wrangle.wrangle_logs(fillna = False)
    no_cohort = altdf[altdf.cohort_id.isna()]
    no_cohort = no_cohort.dropna(axis=0, subset=['ip'])
    plt.figure(figsize=(16, 5)) 
    sns.histplot(data=no_cohort.date, bins = 100)
    plt.title('Curriculum Access for Users with No Cohort')
    plt.show()

def sample_cohort():
    altdf = wrangle.wrangle_logs(fillna = False)
    plt.figure(figsize=(16, 5)) 
    sns.histplot(data=altdf[altdf.cohort_id == 23].date, bins =100)
    plt.title('Example of Normal Curriculum Access for Users from Ulysses Cohort')
    plt.xlim(left = 17500)
    plt.show()