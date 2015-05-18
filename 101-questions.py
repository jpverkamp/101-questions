#!/usr/bin/env python3

import redis
r = redis.StrictRedis(host = 'redis')
r.flushall()

# ----- ------

from models.User import User

u = User('JP', 'me@jverkamp.com', 'password')
print(u)

print('pwd 1', u.verifyPassword('test'))
print('pwd 2', u.verifyPassword('password'))

del u

u = User.load('me@jverkamp.com')
print('pwd 3', u.verifyPassword('password'))

print('name loaded', u['name'])

u2 = User('Aurora', 'princessro07@gmail.com', 'password')
u['friends'].append(u2)
u.save()

del u
del u2

u3 = User.load('me@jverkamp.com')

print(u3['name'], 'is friends with', ', '.join([su['name'] for su in u3['friends']]))

# ----- ------

import sys, time
sys.stdout.flush()
while True:
    time.sleep(1)
