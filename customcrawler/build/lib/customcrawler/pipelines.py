# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from customcrawler.settings import DATABASE_URL
import psycopg2
from customcrawler.models import db_connect
from scrapy.exceptions import DropItem
from customcrawler.models import Quote, URL_details, TimeToCrawl, db_connect
from sqlalchemy.orm import sessionmaker
import random
import requests
from datetime import datetime
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .tasks import process_urls_async



class ScrapyAppPipeline(object):

    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        self.item_scraped_count = 0



    def open_spider(self,spider):
        spider.started_on = datetime.now() # To calculate the time of calling

        session = self.Session()

        try:
            session.execute('''TRUNCATE TABLE main_quote''')
            session.execute('''TRUNCATE TABLE main_url_details''')
            # session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()
        


    def process_item(self, item, spider):

        # session = self.Session()

        # quote = Quote()
        # quote.job_data_id = spider.job_data_id
        # quote.url_content = item["extracted_url"]

        # try:
        #     session.add(quote)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()


        if self.item_scraped_count % 10 == 0 and self.item_scraped_count < 6000:

            print("Scraped Item count", self.item_scraped_count)

            process_urls_async.delay(item["extracted_url"], spider.job_data_id)


        self.item_scraped_count += 1

        return item


    def close_spider(self, spider):

        # work_time = datetime.now() - spider.started_on (Time to Crawl)

        end_time = datetime.now() - spider.started_on

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


