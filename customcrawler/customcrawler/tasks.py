from celery import shared_task
from celery.app.base import Celery
from customcrawler import celeryconfig
from customcrawler.retry_mechanism import retry_session
from customcrawler.models import URL_details
from sqlalchemy.orm import sessionmaker
from customcrawler.models import db_connect
from customcrawler.settings import AXE_CHECKER_URL,CELERY_BROKER_URL
from celery import group
import requests
from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial


# requests.adapters.DEFAULT_RETRIES = 5
# app = Celery('customcrawler', broker=CELERY_BROKER_URL)
# app = Celery('customcrawler',broker='amqp://admin:mypass@rabbitmq:5672',backend='rpc://')
# app.config_from_object(celeryconfig)

session_retry = retry_session(retries=3)
headers = {'User-Agent': 'Mozilla/5.0'}

engine = db_connect()
Session = sessionmaker(bind=engine)
# from requests.adapters import HTTPAdapter

# s = requests.Session()

class ProcessTask(object):

    def __init__(self):
        
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def run(self, base_url, job_data_id):
        
        url = AXE_CHECKER_URL + base_url
        
        # r = session_retry.get(url=url, headers=headers)

        # r = requests.get(url, headers=headers)

        try:
            r = session_retry.get(url=url, headers=headers)
            # r = requests.get(url, headers=headers)
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

        session = self.Session()

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


# @app.task
# def process_urls_async(url, job_data_id):
#     ProcessTask().run(url, job_data_id)


# def processURLsforchecking(reservoir, job_data_id):
#
#     job = group((app.signature(process_urls_async, (url, job_data_id)) for url in reservoir if url))
#     job.apply_async()

def threadProcess(reservoir, job_data_id):
    reservoir = list(filter( bool, reservoir))
    pool = ThreadPool(4)  # Make the Pool of workers
    func = partial(processForLoop, job_data_id)
    pool.map(func, reservoir) #Open the urls in their own threads
    pool.close() #close the pool and wait for the work to finish 
    pool.join()


def processForLoop(job_data_id, base_url):
        
        url = AXE_CHECKER_URL + base_url

        try:
            # while True:
                # try:
                #     r = session_retry.get(url=url, headers=headers)
                #     if r.getcode() == 200:
                #         break
                # except Exception as inst:
                #     print(inst)
            r = session_retry.get(url=url, headers=headers)
            # r = requests.get(url, headers=headers)
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

# @app.task
# def process_urls_async(url, job_data_id):

#     url = "http://axe.checkers.eiii.eu/export-jsonld/pagecheck2.0/?url=" + url
    
#     r = session_retry.get(url=url, headers=headers)

#     data = r.json()

#     total_violations = 0
#     total_verify = 0
#     total_pass = 0

#     for violations in data['result-blob']['violations']:

#         if any("wcag" in w for w in violations['tags']):

#             total_violations += len(violations['nodes'])

#     for incomplete in data['result-blob']['incomplete']:

#         if any("wcag" in w for w in incomplete['tags']):

#             total_verify += len(incomplete['nodes'])

#     for passes in data['result-blob']['passes']:

#         if any("wcag" in w for w in passes['tags']):

#             total_pass += len(passes['nodes'])

#     print("Total Violations", total_violations)
#     print("Total Verify", total_verify)
#     print("Total Pass", total_pass)

    # url_details_item = URLDetails_Item()

    # url_details_item['job_data_id'] = job_data_id

    # url_details_item['site_name'] =  url

    # url_details_item['total_violations'] = total_violations

    # url_details_item['total_verify'] = total_verify

    # url_details_item['total_pass'] = total_pass

    # url_details_item.save()

    # url_details = URL_details()

    # url_details.job_data_id = job_data_id

    # url_details.site_name = url

    # url_details.total_violations = total_violations

    # url_details.total_verify = total_verify

    # url_details.total_pass = total_pass

    # url_details.total_score = str(float("{0:.5f}".format(data['score'])))

    # try:
    #     session.add(url_details)
    #     session.commit()

    # except:
    #     session.rollback()
    #     raise

    # calculated_score = URL_Details(
    #     site_name=value, total_violations=total_violations, total_verify=total_verify, total_pass=total_pass)
    # calculated_score.save()


