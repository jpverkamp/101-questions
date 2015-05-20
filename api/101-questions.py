#!/usr/bin/env python3

# DEBUG
import redis
r = redis.StrictRedis(host = 'redis')
r.flushall()
# /DEBUG

import flask
import inspect
import sys

import controllers
from lib.RESTController import RESTController

app = flask.Flask(__name__)
app.debug = True

for obj_name in dir(controllers):
    cls = getattr(controllers, obj_name)
    if inspect.isclass(cls) and issubclass(cls, RESTController):
        cls(app)

sys.stdout.flush()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8001)
