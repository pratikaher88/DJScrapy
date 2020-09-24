from django.db import models
from django.core.validators import URLValidator


# class Quote(models.Model):
#     """
#     The scrapped data will be saved in this model
#     """
#     job_data_id = models.IntegerField(blank=True, null=True)
#     text = models.TextField()
    

class URL_Details(models.Model):

    job_data_id = models.IntegerField(blank=True, null=True)
    site_name = models.CharField(max_length=1000,validators=[URLValidator()])
    total_violations = models.CharField(max_length=100, blank = True)
    total_verify = models.CharField(max_length=100, blank = True)
    total_pass = models.CharField(max_length=100, blank = True)
    total_score = models.CharField(max_length=100, blank = True)

# class FeedbackInfoInputModel(models.Model):
#     site_name = models.CharField(max_length=500,validators=[URLValidator()])

class TimeToCrawl(models.Model):

    job_data_id = models.IntegerField(blank=True, null=True)
    domain_name = models.TextField()
    time_to_crawl = models.CharField(max_length=100, blank = True)

class Recent_Runs(models.Model):

    job_data_id = models.IntegerField(blank=True, null=True)
    site_name = models.CharField(max_length=1000,validators=[URLValidator()])
    average_score = models.CharField(max_length=100, blank = True, null= True)
    average_time = models.CharField(max_length=100, blank = True, null= True)
