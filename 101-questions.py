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

app.cfg = configparser.ConfigParser()
app.cfg.read('app.cfg')

app.redis = redis.StrictRedis(
    host = app.cfg.get('redis', 'host'),
    port = app.cfg.getint('redis', 'port')
)

import controller.questionset
controller.questionset.register(app)

import controller.user
controller.user.register(app)

if __name__ == '__main__':
    app.secret_key = app.cfg.get('global', 'secret')
    app.run(debug = '--debug' in sys.argv)
