from celery import shared_task
from celery.app.base import Celery
from customcrawler.retry_mechanism import retry_session
from customcrawler.models import URL_details
from sqlalchemy.orm import sessionmaker
from customcrawler.models import db_connect
from customcrawler.settings import AXE_CHECKER_URL,CELERY_BROKER_URL
from celery import group
import requests
from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial
import json
from decouple import config

session_retry = retry_session(retries=3)
headers = {'User-Agent': 'Mozilla/5.0'}

engine = db_connect()
Session = sessionmaker(bind=engine)

def threadProcess(reservoir, job_data_id):
    reservoir = list(filter( bool, reservoir))
    pool = ThreadPool(4)  # Make the Pool of workers
    func = partial(newProcessForLoop, job_data_id)
    pool.map(func, reservoir) #Open the urls in their own threads
    pool.close() #close the pool and wait for the work to finish 
    pool.join()



def newProcessForLoop(job_data_id, base_url):

    data = {
        "url":base_url
        }

    headers = {"content-type":"application/json"}

    response = requests.post('http://axechecker.tingtun.no/check?cb='+config('HOST_NAME_URL')+str(job_data_id), json.dumps(data), headers=headers)

    print(response.text)
