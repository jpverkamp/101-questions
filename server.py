#!/usr/bin/env python3

import sys
if sys.version_info[0] != 3:
    print('Use python3')
    sys.exit()

import flask

app = flask.Flask('101qs')
app.config.update(
    DEBUG='--debug' in sys.argv,
    JSON_AS_ASCII = False,
)

import controller.QuestionSet
controller.QuestionSet.init(app)

@app.route('/', methods = ['get'])
def root():
    return app.send_static_file('index.htm')

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 10177
    )
