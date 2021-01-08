from uuid import uuid4
from urllib.parse import urlparse
# from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import HttpResponse

import random, requests

from random import randint

from main.models import URL_Details,TimeToCrawl,Recent_Runs
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

@require_http_methods(['POST', 'GET']) 
def findDetails(request):

    if request.method == 'POST':
        
        website_name = request.POST.get('website_name')
        crawl_number = request.POST.get('crawl_number')

        job_data_id = randint(10000,99999)

        data = [
        ('project', 'customcrawler'),
        ('spider', 'toscrapespiderax'),
        ('setting', 'CLOSESPIDER_PAGECOUNT='+crawl_number),
        ('setting', 'CLOSESPIDER_TIMEOUT=0'),
        ('limit_count',crawl_number),
        ('job_data_id', job_data_id),
        ('url', website_name)
        ]

        response = requests.post('http://web:6800/schedule.json', data=data)

        return render(request,'crawling_started.html',{'job_data_id': job_data_id})

        # if response.status_code == 200 :
        #     return render(request,'crawling_started.html')

        # status = scrapyd.job_status('default', task)

    
    return render(request,'find_details.html')

    # return render(request,'find_details.html',{'id':1})

# class ListURLDetailsView(generics.ListAPIView):
#     queryset = URL_Details.objects.all()
#     serializer_class = ListURLDetailsSerializer


# class ListCrawledURLsView(generics.ListAPIView):
#     queryset = Quote.objects.all()
#     serializer_class = ListCrawledURLsSerializer


# def viewCrawledResultswithJoBID(request, job_data_id):
#     # print("JID",job_data_id)
#     crawled_objects = Quote.objects.filter(job_data_id=job_data_id)

#     time_to_crawl = TimeToCrawl.objects.filter(job_data_id=job_data_id).first()

#     # try:
#     #     time_to_crawl = TimeToCrawl.objects.get(job_data_id=job_data_id)
#     # except SomeModel.DoesNotExist:
#     #     time_to_crawl = None

#     return render(request,'viewcrawledurls.html', {'details': crawled_objects , 'time_to_crawl' : time_to_crawl})

def viewScoredResultswithJoBID(request, job_data_id):

    crawled_objects = URL_Details.objects.filter(job_data_id=job_data_id)

    avg_list = crawled_objects.values_list('total_score', flat=True)
    
    if crawled_objects.count() > 0:

        average = float("{0:.5f}".format(sum(map(float,list(filter(None, avg_list))))/crawled_objects.count()))
    else:
        average = 0

    return render(request,'viewscoreresults.html', {'details': crawled_objects, 'average' : average })


def viewRecentRuns(request):

    crawled_objects =  Recent_Runs.objects.all()

    return render(request,'viewrecentruns.html', { 'recent_runs_objects': crawled_objects })


@csrf_exempt
@require_POST
def saveScoredURLS(response, jobID):

    print("Response recieved!")

    print("Job ID", jobID)
    # print(request.body)

    data = json.loads(response.body)

    print(data['path'])

    # print(data['url'])
    # for value in data[:5]:
    #     print(value)
    return

    data = data['result']

    url_details = URL_Details()

    url_details.job_data_id = jobID
    url_details.site_name = data['url']
    url_details.total_violations = len(data['inapplicable'])
    url_details.total_verify = len(data['incomplete'])
    url_details.total_pass = len(data['passes'])

    url_details.save()

    return HttpResponse('Saved to DB!')
