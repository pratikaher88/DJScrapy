from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("DATABASE_URL"))


class URL_details(Base):
    __tablename__ = "main_url_details"

    id = Column(Integer, primary_key=True)
    job_data_id = Column('job_data_id', Integer())
    site_name = Column('site_name', Text())
    total_violations = Column('total_violations', Text())
    total_verify = Column('total_verify', Text())
    total_pass = Column('total_pass', Text())
    total_score = Column('total_score', Text())

class TimeToCrawl(Base):
    __tablename__ = "main_timetocrawl"

    id = Column(Integer, primary_key=True)
    job_data_id = Column('job_data_id', Integer())
    domain_name = Column('domain_name', Text())
    time_to_crawl = Column('time_to_crawl', Text())


class Recent_Runs(Base):
    __tablename__ = "main_recent_runs"

    id = Column(Integer, primary_key=True)
    job_data_id = Column('job_data_id', Integer())
    site_name = Column('site_name', Text())
    average_score = Column('average_score', Text())
    average_time = Column('average_time', Text())

