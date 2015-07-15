#!/usr/bin/env python3

import flask
import os
import sys

app = flask.Flask(__name__)
app.debug = True
#app.secret_key = os.urandom(24)
app.secret_key = '\0' * 24 # DEBUG

import controllers
controllers.register_all(app)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8001)
