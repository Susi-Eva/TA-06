import requests
import json
import math
import pandas as pd
from operator import add 
from statistics import mean 
import HandlerAPI
import Prometer
import datetime


def main(repo):
    repo[19:]
    repo = repo[19:]
    repo
    url = "https://github.com/"+repo
    url_issue = "https://api.github.com/repos/"+repo+"/issues?state=all"

    # call function parsed_api
    api_issue = HandlerAPI.parsed_api(url_issue)

    #print(api_issue)

    # selection data api for issue
    parsed_issue = []
    for i in range(len(api_issue)):
        parsed_issue.append((api_issue[i]['id'], api_issue[i]['user']['login'], api_issue[i]['state']))
    Frame_parsedApi = pd.DataFrame(list(parsed_issue), columns=['ID User','User Name','Issue'])


    # call function count issue of developer
    count_state_issues = HandlerAPI.count_state(api_issue)
    Frame_count_state_issues = pd.DataFrame(list(count_state_issues.items()), columns=['User Name','Issue Total'])
    save_issue = Frame_count_state_issues.to_csv(r'app/hasil/issue_count.csv', index = None, header= True)
    df0 = Frame_count_state_issues


    
    url_pull = "https://api.github.com/repos/"+repo+"/pulls?state=all"

    api_pull = HandlerAPI.parsed_api(url_pull)

    # selection data api for pull_request
    parsed_pull = []
    for i in range(len(api_pull)):
        parsed_pull.append((api_pull[i]['id'], api_pull[i]['user']['login'], api_pull[i]['state']))

    # data make to frame
    Frame_parsedApi_pull = pd.DataFrame(list(parsed_pull), columns=['ID User','User Name','Pull'])
    count_state_pulls = HandlerAPI.count_state(api_pull)
    Frame_count_state_pulls = pd.DataFrame(list(count_state_pulls.items()), columns=['User Name','PR Total'])
    save_pull = Frame_count_state_pulls.to_csv(r'app/hasil/pull_count.csv', index = None, header= True)
    df1 = Frame_count_state_pulls


    urlCommit = "https://api.github.com/repos/"+repo+"/stats/contributors"

    api_commit = HandlerAPI.parsed_api(urlCommit)

    parsed_commit = []
    for i in range(len(api_commit)):
        parsed_commit.append((api_commit[i]['author']['id'], api_commit[i]['author']['login'], api_commit[i]['total']))
        
    # data make to frame
    Frame_parsedApi_commit = pd.DataFrame(list(parsed_commit), columns=['ID User','User Name','Commit'])

    # call function count issur of developer
    # count_state_dev_commit = count_state_commit(api_commit)
    # data make to frame
    # Frame_count_state_commit = pd.DataFrame(list(count_state_dev_commit.items()), columns=['User Name','Commit Total'])
    Frame_parsedApi_commit = pd.DataFrame(list(parsed_commit), columns=['ID User','User Name','Commit Total'])
    Frame_count_state_commit = Frame_parsedApi_commit
    save_commit = Frame_count_state_commit.to_csv(r'app/hasil/commit_count.csv', index = None, header= True)
    df2 = Frame_count_state_commit

    count_state_dev_LOC = HandlerAPI.count_loc(api_commit)
    frame_LOC = pd.DataFrame(list(count_state_dev_LOC.items()), columns=['User Name', 'LOC Total'])
    save_loc = frame_LOC.to_csv(r'app/hasil/loc_count.csv', index = None, header= True)
    df3 = frame_LOC

    merge0 = pd.merge(df0, df1, on='User Name', how='outer')
    merge0.fillna(0, inplace = True)

    merge1 = pd.merge(pd.merge(df2, df3), merge0, on = 'User Name', how='outer')
    merge1.fillna(0, inplace = True)

    dftest0 = pd.DataFrame(merge1["Issue Total"])
    dftest1 = pd.DataFrame(merge1["PR Total"])
    dftest2 = pd.DataFrame(merge1["Commit Total"])
    dftest3 = pd.DataFrame(merge1["LOC Total"])
    dftest4 = pd.DataFrame(merge1["User Name"])

    issue_score = Prometer.performance_issue(dftest0)
    issue_score = issue_score['issue_score']

    pulls_score = Prometer.performance_pull(dftest1)
    pulls_score = pulls_score['pull_score']

    commit_score = Prometer.performance_commit(dftest2)
    commit_score = commit_score['commit_score']

    loc_score = Prometer.performance_LOC(dftest3)
    loc_score = loc_score['loc_score']

    merge1['Issue Score'] = pd.DataFrame(issue_score)
    merge1['PR Score'] = pd.DataFrame(pulls_score)
    merge1['Commit Score'] = pd.DataFrame(commit_score)
    merge1['LOC Score'] = pd.DataFrame(loc_score)

    Total = Prometer.Total(merge1)

    merge1['Total Performance of Programmer'] = Total

    columnTitle = ['User Name', 'PR Total', 'PR Score', 'Issue Total', 'Issue Score', 'Commit Total', 'Commit Score', 'LOC Total', 'LOC Score', 'Total Performance of Programmer']
    frame = merge1.reindex(columns = columnTitle)
    hasil = frame.to_csv(r'app/hasil/hasil.csv', index = None, header= True)
    
    # data = [['GitHub URL',url] , ['Time for Retrieving', datetime.datetime.now()] ,['Total Contributor',len(issue_score)], ['Total Pull Requests Scores', merge1['PR Score'].sum()] , ['Total Issues Scores', merge1['Issue Score'].sum()], ['Total Commits Score', merge1['Commit Score'].sum()] , ['Total LOC  Score', merge1['LOC Score'].sum()], ['Highest Performance Score', merge1['Total Performance of Programmer'].max()], ['Lowest Performance Score', merge1['Total Performance of Programmer'].min()], ['Average Performance Score', merge1['Total Performance of Programmer'].mean()]]
    data = {'Komponen': ['GitHub URL', 'Time for Retrieving', 'Total Contributor', 'Total Pull Requests Scores', 'Total Issues Scores', 'Total Commits Score', 'Total LOC  Score', 'Highest Performance Score', 'Lowest Performance Score', 'Average Performance Score'],
            'Keterangan': [url, datetime.datetime.now(), len(issue_score), merge1['PR Score'].sum(), merge1['Issue Score'].sum(), merge1['Commit Score'].sum(), merge1['LOC Score'].sum(), merge1['Total Performance of Programmer'].max(), merge1['Total Performance of Programmer'].min(), round(merge1['Total Performance of Programmer'].mean(), 3)]}
    df = pd.DataFrame(data)  

    deskripsi_frame = df.to_csv('app/hasil/deskripsi.csv', index=None, header=True)  
    
    return

        