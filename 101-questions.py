#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import flask
import json
import os
import redis
import sys

app = flask.Flask('101-questions')
app.checkPermissions = True

class unsafe(object):
    depth = 0

    def __enter__(self):
        unsafe.depth += 1
        app.checkPermissions = False

    def __exit__(self, type, value, traceback):
        unsafe.depth -= 1
        if unsafe.depth == 0:
            app.checkPermissions = True

app.unsafe = unsafe

app.cfg = configparser.ConfigParser()
app.cfg.read('app.cfg')

app.redis = redis.StrictRedis(
    host = app.cfg.get('redis', 'host'),
    port = app.cfg.getint('redis', 'port')
)

import controller.user
controller.user.register(app)

import controller.questionset
controller.questionset.register(app)

if __name__ == '__main__':
    app.secret_key = app.cfg.get('global', 'secret')
    app.run(debug = '--debug' in sys.argv)
