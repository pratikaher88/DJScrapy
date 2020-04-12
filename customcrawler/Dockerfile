FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /scrapyd_service

WORKDIR /scrapyd_service

ADD . /scrapyd_service/

RUN pip install -r requirements.txt

# RUN apt-get update && apt-get install -y python-dev python-pip python-setuptools libffi-dev libxml2-dev libxslt1-dev 
# RUN apt-get purge pip3

# ADD requirements.txt /tmp/requirements.txt
# RUN pip3 install -r /tmp/requirements.txt

# RUN apt-get update
# RUN apt-get install rabbitmq-server -y
  
EXPOSE 6800
# EXPOSE 5672
# COPY ./scrapyd.conf /etc/scrapyd/

# CMD [ "scrapyd" ]

# ENTRYPOINT celery -A customcrawler worker --concurrency=20 --loglevel=DEBUG


# ENTRYPOINT celery -A customcrawler worker --loglevel=DEBUG
