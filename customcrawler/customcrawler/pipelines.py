# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from customcrawler.models import URL_details, TimeToCrawl, db_connect, Recent_Runs
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# from .tasks import process_urls_async, processURLsforchecking, processForLoop, threadProcess
from .tasks import threadProcess
import random
import time 

class ScrapyAppPipeline(object):

    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        self.item_scraped_count = 0
        self.reservoir = [False]*600
        # self.reservoir_size = 600

    def open_spider(self,spider):
        self.started_on = datetime.now() # To calculate the time of calling

        session = self.Session()

        try:
            # session.execute('''TRUNCATE TABLE main_quote''')
            session.execute('''TRUNCATE TABLE main_url_details''')
            session.execute('''TRUNCATE TABLE main_recent_runs''')
            # session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()
        


    def process_item(self, item, spider):


        if self.item_scraped_count < 600:
            
            self.reservoir[self.item_scraped_count] = item['extracted_url']


        elif self.item_scraped_count < 6000:

            j = random.randrange(self.item_scraped_count + 1)

            if j < 600:
                self.reservoir[j] = item['extracted_url']

        self.item_scraped_count+=1

        # if self.item_scraped_count < 6000 and self.item_scraped_count % 10 == 0:

        #     print("Scraped Item count", self.item_scraped_count)

        #     process_urls_async.delay(item["extracted_url"], spider.job_data_id)

        # self.item_scraped_count += 1

        return item


    def close_spider(self, spider):

        print(self.reservoir, spider.limit_count)

        threadProcess(self.reservoir[:int(spider.limit_count)], spider.job_data_id)

        # end_time = datetime.now() - spider.started_on
        
        # print("%s:%s.%s" % (end_time.hour  , end_time.minute, end_time.second))

        end_time = datetime.now() - self.started_on

        # print(self.started_on)

        session = self.Session()

        recent_runs = Recent_Runs()

        recent_runs.job_data_id = spider.job_data_id

        recent_runs.site_name = spider.domain

        recent_runs.average_time = end_time
        recent_runs.average_score = 99

        try:
            session.add(recent_runs)
            session.commit()
        except:
            session.rollback()
            raise

        session.close()

        session = self.Session()

        time_to_crawl = TimeToCrawl()

        time_to_crawl.job_data_id = spider.job_data_id

        time_to_crawl.domain_name = spider.domain

        time_to_crawl.time_to_crawl = end_time

        try:
            session.add(time_to_crawl)
            session.commit()

        except:
            session.rollback()
            raise

        session.close()


