import requests
import json
import math
import pandas as pd
from operator import add 
from statistics import mean 
import HandlerAPI
import Prometer
import datetime
import arrow
import numpy as np
import import_ipynb
from datetime import datetime, timedelta


def main(repo):
    repo[19:]
    repo = repo[19:]
    repo
    url = "https://github.com/"+repo

    api_repo = HandlerAPI.parsed_api(url)
    dt_created = api_repo['created_at']
    dt = arrow.get(dt_created)
    dt_upt=dt.date()
    dt_upt = pd.to_datetime(dt_upt)

    numberOfWeekday = dt_upt.weekday()
    if numberOfWeekday != 6:
        dt_upt = dt_upt - timedelta(days=numberOfWeekday+1)

    didx = pd.DatetimeIndex(start =dt_upt, freq ='W',  
                            periods = 2)

    url_issue = "https://api.github.com/repos/"+repo+"/issues?state=all"

    # call function parsed_api
    api_issue = HandlerAPI.parsed_api(url_issue)

    #print(api_issue)

    # selection data api for issue
    parsed_issue = []
    for i in range(len(api_issue)):
        parsed_issue.append((api_issue[i]['id'], api_issue[i]['user']['login'], api_issue[i]['state']))
    Frame_parsedApi = pd.DataFrame(list(parsed_issue), columns=['ID User','User Name','Issue'])

    Frame_parsedApi['date'] = Frame_parsedApi["Created_at"].apply( lambda Frame_parsedApi : 
    datetime(year=Frame_parsedApi.year, month=Frame_parsedApi.month, day=Frame_parsedApi.day))
    df_agg_issue = Frame_parsedApi.groupby(['User Name','date'] ,as_index=False).agg({"Issue":"count"})

    today = datetime.today()
    print ('Today    :', today)
    one_day = timedelta(days=1)
   
    WeeklyIssue = HandlerAPI.countIssue(dt_upt, df_agg_issue)

    for i in range(WeeklyIssue):
        open_csv = pd.read_csv('E:/Materi Kuliah/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Issue/Base/issue_week{counter}.csv'.format(counter = i+1))
        issue_score = Prometer.performance_issue(open_csv)
        issue_score = issue_score.replace(np.NaN, 0)
        save = issue_score.to_csv(r'E:/Materi Kuliah/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Issue/Derivative/issue_score_week{counter}.csv'.format(counter = i+1), index = None, header= True)


    # call function count issue of developer
    # count_state_issues = HandlerAPI.count_state(api_issue)
    # Frame_count_state_issues = pd.DataFrame(list(count_state_issues.items()), columns=['User Name','Issue Total'])
    # save_issue = Frame_count_state_issues.to_csv(r'app/hasil/issue_count.csv', index = None, header= True)
    # df0 = Frame_count_state_issues


    
    url_pull = "https://api.github.com/repos/"+repo+"/pulls?state=all"

    api_pull = HandlerAPI.parsed_api(url_pull)

    # selection data api for pull_request
    parsed_pull = []
    for i in range(len(api_pull)):
        parsed_pull.append((api_pull[i]['id'], api_pull[i]['user']['login'], api_pull[i]['state']))

    # data make to frame
    Frame_parsedApi_pull = pd.DataFrame(list(parsed_pull), columns=['ID User','User Name','Pull'])
    Frame_pull['date'] = Frame_pull["Created_at"].apply( lambda Frame_pull : 
    datetime(year=Frame_pull.year, month=Frame_pull.month, day=Frame_pull.day))
    df_agg_pull = Frame_pull.groupby(['User Name','date'] ,as_index=False).agg({"Pull":"count"})
    WeeklyPR = HandlerAPI.countPR(dt_upt, df_agg_pull)
    for i in range(WeeklyPR):
        open_csv = pd.read_csv('E:/Susii Eva Maria/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Pull/Base/PR_week{counter}.csv'.format(counter = i+1))
        pull_score = Prometer.performance_pull(open_csv)
        pull_score = pull_score.replace(np.NaN, 0)
        save = pull_score.to_csv(r'E:/Susii Eva Maria/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Pull/Derivative/PR_score_week{counter}.csv'.format(counter = i+1), index = None, header= True)


    urlCommit = "https://api.github.com/repos/"+repo+"/stats/contributors"

    api_commit = HandlerAPI.parsed_api(urlCommit)

    parsed_commit = []
    for i in range(len(api_commit)):
        parsed_commit.append((api_commit[i]['author']['id'], api_commit[i]['author']['login'], api_commit[i]['total']))
        
    # data make to frame
    Frame_parsedApi_commit = pd.DataFrame(list(parsed_commit), columns=['ID User','User Name','Commit'])

    WeeklyCommit = HandlerAPI.countCommit(api_contributor)

    weekContributor = len(api_cotributor[0]['weeks'])

    for i in range(weekContributor):
        open_csv = pd.read_csv('E:/Susii Eva Maria/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Commit/Base/commit_week{counter}.csv'.format(counter = i+1))
        commits_score = Prometer.performance_commit(open_csv)
        commits_score = commits_score.replace(np.NaN, 0)
        save = commits_score.to_csv(r'E:/Susii Eva Maria/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Commit/Derivative/commit_score_week{counter}.csv'.format(counter = i+1), index = None, header= True)
    # count_state_dev_LOC = HandlerAPI.count_loc(api_commit)
    # frame_LOC = pd.DataFrame(list(count_state_dev_LOC.items()), columns=['User Name', 'LOC Total'])
    # save_loc = frame_LOC.to_csv(r'app/hasil/loc_count.csv', index = None, header= True)
    # df3 = frame_LOC

    # merge0 = pd.merge(df0, df1, on='User Name', how='outer')
    # merge0.fillna(0, inplace = True)

    # merge1 = pd.merge(pd.merge(df2, df3), merge0, on = 'User Name', how='outer')
    # merge1.fillna(0, inplace = True)

    # dftest0 = pd.DataFrame(merge1["Issue Total"])
    # dftest1 = pd.DataFrame(merge1["PR Total"])
    # dftest2 = pd.DataFrame(merge1["Commit Total"])
    # dftest3 = pd.DataFrame(merge1["LOC Total"])
    # dftest4 = pd.DataFrame(merge1["User Name"])

    # issue_score = Prometer.performance_issue(dftest0)
    # issue_score = issue_score['issue_score']

    # pulls_score = Prometer.performance_pull(dftest1)
    # pulls_score = pulls_score['pull_score']

    # commit_score = Prometer.performance_commit(dftest2)
    # commit_score = commit_score['commit_score']

    # loc_score = Prometer.performance_LOC(dftest3)
    # loc_score = loc_score['loc_score']

    # merge1['Issue Score'] = pd.DataFrame(issue_score)
    # merge1['PR Score'] = pd.DataFrame(pulls_score)
    # merge1['Commit Score'] = pd.DataFrame(commit_score)
    # merge1['LOC Score'] = pd.DataFrame(loc_score)

    # Total = Prometer.Total(merge1)

    # merge1['Total Performance of Programmer'] = Total

    mergeWeeklyData = Prometer.Total(weekContributor)
    # hasil = frame.to_csv(r'app/hasil/hasil.csv', index = None, header= True)
    
    # data = [['GitHub URL',url] , ['Time for Retrieving', datetime.datetime.now()] ,['Total Contributor',len(issue_score)], ['Total Pull Requests Scores', merge1['PR Score'].sum()] , ['Total Issues Scores', merge1['Issue Score'].sum()], ['Total Commits Score', merge1['Commit Score'].sum()] , ['Total LOC  Score', merge1['LOC Score'].sum()], ['Highest Performance Score', merge1['Total Performance of Programmer'].max()], ['Lowest Performance Score', merge1['Total Performance of Programmer'].min()], ['Average Performance Score', merge1['Total Performance of Programmer'].mean()]]
    data = {'Komponen': ['GitHub URL', 'Time for Retrieving', 'Total Contributor', 'Total Pull Requests Scores', 'Total Issues Scores', 'Total Commits Score', 'Total LOC  Score', 'Highest Performance Score', 'Lowest Performance Score', 'Average Performance Score'],
            'Keterangan': [url, datetime.datetime.now(), len(issue_score), merge1['PR Score'].sum(), merge1['Issue Score'].sum(), merge1['Commit Score'].sum(), merge1['LOC Score'].sum(), merge1['Total Performance of Programmer'].max(), merge1['Total Performance of Programmer'].min(), round(merge1['Total Performance of Programmer'].mean(), 3)]}
    df = pd.DataFrame(data)  

    deskripsi_frame = df.to_csv('app/hasil/deskripsi.csv', index=None, header=True)  
    
    return

        