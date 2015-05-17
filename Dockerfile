FROM python:3

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y cron

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

ADD . /app

RUN crontab /app/crontab
RUN touch /var/log/cron.log

CMD cron && ./server.py
