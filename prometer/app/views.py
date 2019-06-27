from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from app import main
import pandas as pd
import json

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def process(request):
    if request.method == 'POST':
        repoName = request.POST['repo']
        call_func = main.main(repoName)

        return HttpResponseRedirect('/result/') 

def result(request):

    open_deskipsi = pd.read_csv('app/hasil/deskripsi.csv', engine='python')
    deskipsi_frame = open_deskipsi.to_html(index=False, classes='table table-responsive')

    issue = pd.read_csv('app/hasil/hasil.csv', engine='python')
    to_frame_issue = issue.to_html(index=False, classes='table table-striped table-hover" id = "tableExample3')

    content={
        'issue' : to_frame_issue,
        'deskripsi' : deskipsi_frame,
    }

    return render(request, 'app/data.html', content)




def toJSON(request):
    issue = pd.read_csv('app/hasil/hasil.csv', engine='python')
    toJSON = issue.to_json('app/hasil/hasil.json', orient='index')
    with open('app/hasil/hasil.json') as f:
        data = json.load(f)
    content={
        'data' : data
    }
    return render(request, 'app/toJSON.html', content)

# def error(request):
#     return render(request, 'app/error.html')
