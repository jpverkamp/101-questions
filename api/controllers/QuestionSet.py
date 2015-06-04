import base64
import flask
import functools
import json
import os
import random

from flask.ext.api import status

import utils

questionset_api = flask.Blueprint('questionset_api', __name__, url_prefix='/api/questionset')

# user:<email>:questionsets is a list of questionsets for a user
# questionset:<id> is metadata for a questionset
# questionset:<id>:questions is a list of questions

def current_user():
    if not 'email' in flask.session:
        flask.abort(status.HTTP_401_UNAUTHORIZED, 'Not logged in')

    return flask.session['email']

def get_questionset(id):

    owner = current_user()

    r = utils.redis()

    qs_key = 'questionset:' + id
    qsq_key = 'questionset:{email}:questions'.format(email = owner)

    if not r.exists(qs_key):
        flask.abort(status.HTTP_404_NOT_FOUND, 'QuestionSet does not exist')

    qs = r.hgetall(qs_key)

    if owner != qs['owner']:
        flask.abort(status.HTTP_403_FORBIDDEN, 'QuestionSet is not yours')

    qs['question-count'] = r.llen(qsq_key)
    return qs

# --- global ---

@questionset_api.route('/', methods = ['GET'])
def list_questionset():

    r = utils.redis()
    uqs_key = 'user:{email}:questionsets'.format(email = current_user())

    return json.dumps(r.lrange(uqs_key, 0, -1))

# --- questionset level ---

@questionset_api.route('/', methods = ['PUT'])
def create_questionset():

    r = utils.redis()

    owner = current_user()
    title = flask.request.form['title']
    start_date = flask.request.form['start-date']
    frequency = flask.request.form['frequency']

    qs_key = None
    while not qs_key or r.exists(qs_key):
        id = base64.urlsafe_b64encode(os.urandom(15)).decode('utf-8')
        qs_key = 'questionset:{id}'.format(id = id)

    r.hset(qs_key, 'owner', owner)
    r.hset(qs_key, 'title', title)
    r.hset(qs_key, 'start-date', start_date)
    r.hset(qs_key, 'frequency', frequency)

    uqs_key = 'user:{email}:questionsets'.format(email = owner)
    r.rpush(uqs_key, id)

    return json.dumps(id)

@questionset_api.route('/<id>', methods = ['GET'])
def rest_get_questionset(id):

    qs = get_questionset(id)
    return json.dumps(qs)

@questionset_api.route('/<id>', methods = ['DELETE'])
def delete_questionset(id):

    # Permission checks
    get_questionset(id)

    uqs_key = 'questionsets:{email}'.format(email = current_user())
    qs_key = 'questionset:{id}'.format(id = id)
    qsq_key = 'questionset:{id}:questions'.format(id = id)

    r.lrem(uqs_key, id)
    r.delete(qs_key)
    r.delete(qsq_key)

    return json.dumps(True)

@questionset_api.route('/<id>', methods = ['POST'])
def update_questionset(id):

    # Permission checks
    get_questionset(id)
    qs_key = 'questionset:{id}'.format(id = id)

    for field in ('title', 'start-date', 'frequency'):
        if field in flask.request.form:
            r.hset(qs_key, field, flask.request.form[field])

    return json.dumps(True)

# --- individual questions ---

@questionset_api.route('/<id>/question', methods = ['PUT'])
def add_question(id):

    # Permission checks
    qs = get_questionset(id)

    text = flask.request.form['text']
    r.rpush(q_key, text)

    return json.dumps(True)

@questionset_api.route('/<id>/question/<index>', methods = ['DELETE'])
def remove_question(id, index):

    # Permission checks
    qs = get_questionset(id)

    text = flask.request.form['text']
    r.rpush(q_key, text)

    qsq_key = 'questionset:{id}:questions'.format(id = id)

    r.lset(qsq_key, index, '__DELETED__')
    r.lrem(qsq_key, '__DELETED__')

    return json.dumps(True)

@questionset_api.route('/<id>/question/<index>', methods = ['POST'])
def modify_question(id, index):

    # Permission checks
    qs = get_questionset(id)

    text = flask.request.form['text']
    r.rpush(q_key, text)

    qsq_key = 'questionset:{id}:questions'.format(id = id)

    text = flask.request.form['text']
    r.lset(qsq_key, index, text)

    return json.dumps(True)
