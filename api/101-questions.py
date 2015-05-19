#!/usr/bin/env python3

import redis
r = redis.StrictRedis(host = 'redis')
r.flushall()

# ----- ------

import datetime
import pprint

from models import *

u = User('JP', 'me@jverkamp.com', 'password')
print(u)

print('pwd 1', u.verifyPassword('test'))
print('pwd 2', u.verifyPassword('password'))

del u

u = User.load('me@jverkamp.com')
print('pwd 3', u.verifyPassword('password'))

print('name loaded', u['name'])

u2 = User('Aurora', 'princessro07@gmail.com', 'password')
u.save()

del u
del u2

u3 = User.load('me@jverkamp.com')

qss = []
for i in range(3):
    qss.append(QuestionSet(title = 'Test qs ' + str(i), questions = [Question('test ' + str(j)) for j in range(10)]))

qr = QuestionRun(
    title = 'test',
    start_date = str(datetime.datetime.now()),
    frequency = 'daily',
    users = [u3, User.load('princessro07@gmail.com')],
    questionsets = qss
)
pprint.pprint(qr.data)
qr.save()

print(qr)

del qr
del qss

# ----- ------

import sys, time
sys.stdout.flush()
while True:
    time.sleep(1)
