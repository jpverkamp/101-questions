#!/usr/bin/env python3

import flask
import os
import signal
import sys

app = flask.Flask(__name__)

DEBUG_MODE = ('--debug' in sys.argv) or ('101QS_DEBUG' in os.environ)
if DEBUG_MODE: print('Running in DEBUG_MODE')

RELOAD_MODE = ('--reload' in sys.argv) or ('101QS_RELOAD' in os.environ)
if RELOAD_MODE: print('Running in RELOAD_MODE')

sys.stdout.flush()

# Use a terrible, consistent key for debug mode
# In production mode, generate a new key on every deploy (will log everyone out)
if DEBUG_MODE:
    app.secret_key = '\0' * 24
else:
    app.secret_key = os.urandom(24)

import controllers
controllers.register_all(app)

import workers
workers.register_all(app)

def sigterm_handler(signo, frame):
    print('Exiting, force Redis SAVE')
    redis = redis.StrictRedis(host = 'redis', decode_responses = True)
    redis.save()

signal.signal(signal.SIGTERM, sigterm_handler)

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 8001,
        debug = DEBUG_MODE,
        use_reloader = RELOAD_MODE,
    )
