FROM python:3

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .
CMD python 101-questions.py
