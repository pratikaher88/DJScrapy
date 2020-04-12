from django.urls import path
# from main.views import (displayModelObjects,displayCalculatedScores,sendRequestToAPI,viewScoreResults
# ,findDetails, ListURLDetailsView, ListCrawledURLsView
# ,viewCrawledResults, viewCrawledResultswithJoBID, viewScoredResultswithJoBID)
from main.views import (findDetails, viewScoredResultswithJoBID)


urlpatterns = [

path('',findDetails,name='find-details'),
# path('display', displayModelObjects, name='display-results'),
# path('calculatescores', displayCalculatedScores, name='calcaulate-scores'),
# path('viewscoredresults', viewScoreResults, name='view-scored-results'),
path('viewscoredresults/<int:job_data_id>', viewScoredResultswithJoBID, name='view-scored-results-with-jobid'),
# path('viewcrawledresults', viewCrawledResults, name='view-crawled-results'),
# path('viewcrawledresults/<int:job_data_id>', viewCrawledResultswithJoBID, name='view-crawled-results-with-jobid'),
# path('sendreqtoapi', sendRequestToAPI, name='send-request-to-api'),
# path('clearquote', clearQuote, name='clear-quote'),
# path('viewdetails', ListURLDetailsView.as_view(), name='list-url-details'),
# path('viewcrawledurls', ListCrawledURLsView.as_view(), name='list-url-details'),

]

