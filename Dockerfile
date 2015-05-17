FROM python:3

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y cron

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD crontab /etc/cron.d/101-questions/
RUN chmod 0644 /etc/cron.d/101-questions

ADD . /app

CMD cron && python3 server.py
