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



def processForLoop(job_data_id, base_url):
        
        url = AXE_CHECKER_URL + base_url

        try:
            r = session_retry.get(url=url, headers=headers)
        except:
            return

        if r.status_code == 504:
            return
    
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

        session = Session()

        url_details = URL_details()

        url_details.job_data_id = job_data_id

        url_details.site_name = base_url

        url_details.total_violations = total_violations

        url_details.total_verify = total_verify

        url_details.total_pass = total_pass

        url_details.total_score = str(float("{0:.5f}".format(data['score'])))

        try:
            session.add(url_details)
            session.commit()

        except:
            session.rollback()
            raise

        session.close()

        print(base_url, job_data_id)
