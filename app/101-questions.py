#!/usr/bin/env python3

# DEBUG
import redis
r = redis.StrictRedis(host = 'redis')
r.flushall()
# /DEBUG

import flask
import os
import sys

app = flask.Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)

import controllers
app.register_blueprint(controllers.user_api)
app.register_blueprint(controllers.questionset_api)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8001)
