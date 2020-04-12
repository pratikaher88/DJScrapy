from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
import random, requests
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from rest_framework import generics
from .serializers import ListURLDetailsSerializer
from random import randint

# from main.utils import URLUtil
# from main.models import ScrapyItem
from main.models import URL_Details,TimeToCrawl

def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False

    return True



# def displayModelObjects(request):

#     objects_quote = Quote.objects.all()

#     return render(request,'display_quotes.html', {'details': objects_quote })



# def viewScoreResults(request):
    
#     calculated_objects = URL_Details.objects.all()
    
#     average = sum(map(float,list(filter(None, URL_Details.objects.values_list('total_score', flat=True)))))

#     # average = sum(map(int, URL_Details.objects.all().values_list('total_score', flat=True)))
    
#     return render(request,'viewscoreresults.html', {'details': calculated_objects,'average' : average })


# def viewCrawledResults(request):
    
#     crawled_objects = Quote.objects.all()
    
#     return render(request,'viewcrawledurls.html', {'details': crawled_objects })



# def displayCalculatedScores(request): 

#     url_details = URL_Details.objects.all()

#     return render(request,'calculate_scores.html', {'details': url_details })

# def sendRequestToAPI(request):

#     Quote.objects.all().delete()

#     try:
#         task = scrapyd.schedule('default', 'toscrape-css')

#     except Exception :
#         pass
#         # print(e)
#         # if e == scrapy_error: 
#         #     print("Hello")
#         # 
#     # objects_quote = Quote.objects.all()
#     # return render(request,'display_quotes.html', {'details': objects_quote })
#     return redirect(reverse('display-results'))
        
# # def clearQuote(request):

#     Quote.objects.all().delete()

#     return None


@require_http_methods(['POST', 'GET']) 
def findDetails(request):

    if request.method == 'POST':
        
        website_name = request.POST.get('website_name')

        crawl_number = request.POST.get('crawl_number')

        # print("Website Name",website_name)

        job_data_id = randint(10000,99999)

        # print("JDIT", job_data_id)

        data = [
        ('project', 'customcrawler'),
        ('spider', 'toscrapespiderax'),
        ('setting', 'CLOSESPIDER_PAGECOUNT='+crawl_number),
        ('setting', 'CLOSESPIDER_TIMEOUT=0'),
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


    # return render(request,'find_details.html')


# def csd():

    array_urls = Quote.objects.values_list('text', flat=True)
    array_urls = list(array_urls)
    
    score_urls = random.sample(array_urls, 10)

    for value in iter(score_urls):



        url = "http://axe.checkers.eiii.eu/export-jsonld/pagecheck2.0/?url=" + value

        r = requests.get(url=url)
        data = r.json()


        total_violations = 0
        total_verify = 0
        total_pass = 0

        for violations in data['result-blob']['violations']:

            if any("wcag" in w for w in violations['tags']):

                total_violations += len(violations['nodes'])


        for incomplete in data['result-blob']['incomplete']:

            if any("wcag" in w for w in incomplete['tags']):

                total_verify += len(incomplete['nodes'])


        for passes in data['result-blob']['passes']:

            if any("wcag" in w for w in passes['tags']):

                total_pass += len(passes['nodes'])

        
        calculated_score = URL_Details(site_name=value, total_violations = total_violations,total_verify = total_verify
                                            ,total_pass = total_pass)
        calculated_score.save()

    return render(request,'calculate_scores.html', {'details': calculated_objects })



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
    
    # print("JID",job_data_id)

    crawled_objects = URL_Details.objects.filter(job_data_id=job_data_id)

    avg_list = crawled_objects.values_list('total_score', flat=True)
    
    if crawled_objects.count() > 0:

        average = float("{0:.5f}".format(sum(map(float,list(filter(None, avg_list))))/crawled_objects.count()))
    else:
        average = 0

    return render(request,'viewscoreresults.html', {'details': crawled_objects, 'average' : average })


