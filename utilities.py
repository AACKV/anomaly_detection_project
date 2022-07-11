import requests
import os
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

    print("The two largest subgroups are as follows:\n"
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

    print("The largest subgroups are as follows:\n"
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



def accessed_once_series(the_df):
    df = pd.Series((the_df.path.value_counts()==1).index, name='paths').dropna()
    return df

def least_accessed(the_df):
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

def other_topics(the_df):
    df = accessed_once_series(the_df)
    
    topics = ['sql', 'python', 'stats', 'fundamentals', 'regression', 'clustering', 'nlp',
              'appendix', 'timeseries', 'anomaly', 'classification', 'spark', 'storytelling', 'javascript', 'java',
             'css', 'spring', 'jquery', 'capstone', 'php', 'cli', 'git', 'laravel', 'angular', 'web-design', 'prework',
             'apache', 'django', 'other_topics', 'pre-work']

    all_topics_reg_ex = '|'.join(topics)
    
    df= df[~df.str.contains(all_topics_reg_ex, case=False)]
    
    return df

def without_file_pages(the_df):
    series = accessed_once_series(the_df)
    files = ['.html', '.json', '.aspx', '.jpg', '.jpeg', '.png', '.csv', '.mov', '.zip', 'slides', '.md', '.txt',
             '.ico']
    files = [file+ '$' if file != 'slides' else file for file in files]
    files = '|'.join(files)
    
    series = series[~series.str.contains(files)]
    
    return series


def create_least_viewed_viz(df):
    least= least_accessed(df)

    plt.title('Subject Frequency in Least Viewed Pages')
    sns.barplot(data= least[:6], x = 'topic', y = 'num_times_accessed')
    