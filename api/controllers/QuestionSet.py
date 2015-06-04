import flask
import functools
import json
import random
import redis
import uuid

questionset_api = flask.Blueprint('questionset_api', __name__, url_prefix='/api/questionset')

# user:<email>:questionsets is a list of questionsets for a user
# questionset:<id> is metadata for a questionset
# questionset:<id>:questions is a list of questions

def current_user():
    if not 'email' in flask.session:
        flask.abort(401, 'Not logged in')

    return flask.session['email']

def get_questionset(id):

    r = redis.StrictRedis(host = 'redis')

    qs_key = 'questionset:' + id
    qsq_key = 'questionset:{id}:questions'.format(id)

    if not r.exists(qs_key):
        flask.abort(404, 'QuestionSet does not exist')

    qs = r.hgetall(qs_key)

    if current_user != qs['owner']:
        flask.abort(403, 'QuestionSet is not yours')

    qs['question-count'] = r.llen(qsq_key)
    return qs

# --- global ---

@questionset_api.route('/', methods = ['GET'])
def list_questionset():

    r = redis.StrictRedis(host = 'redis')
    uqs_key = 'user:{email}:questionsets'.format(email = current_user())

    return json.dumps(r.lrange(email, uqs_key, 0, -1))

# --- questionset level ---

@questionset_api.route('/<id>', methods = ['PUT'])
def create_questionset(id):

    r = redis.StrictRedis(host = 'redis')

    owner = current_user()
    title = flask.request.form['title']
    start_date = flask.request.form['start-date']
    frequency = flask.request.form['frequency']
    id = base64.b64encode(os.urandom(15))

    qs_key = None
    while not rkey or r.exists(qs_key):
        id = base64.b64encode(os.urandom(15))
        qs_key = 'questionset:' + id

    r.hset(qs_key, 'owner', owner)
    r.hset(qs_key, 'title', title)
    r.hset(qs_key, 'start-date', start_date)
    r.hset(qs_key, 'frequency', frequency)

    uqs_key = 'user:{email}:questionsets'.format(email = email)
    h.rpush(uqs_key, id)

@questionset_api.route('/<id>', methods = ['GET'])
def get_questionset(id):

    qs = get_questionset(id)
    return json.dumps(qs)

@questionset_api.route('/<id>', methods = ['DELETE'])
def delete_questionset(id):

    # Permission checks
    get_questionset(id)

    uqs_key = 'questionsets:{email}'.format(email = current_user())
    qs_key = 'questionset:{id}'.format(id)
    qsq_key = 'questionset:{id}:questions'.format(id)

    r.lrem(uqs_key, id)
    r.delete(qs_key)
    r.delete(qsq_key)

@questionset_api.route('/<id>', methods = ['POST'])
def update_questionset(id):

    # Permission checks
    get_questionset(id)
    qs_key = 'questionset:{id}'.format(id)

    for field in ('title', 'start-date', 'frequency'):
        if field in flask.request.form:
            r.hset(qs_key, field, flask.request.form[field])

# --- individual questions ---

@questionset_api.route('/<id>/question', methods = ['PUT'])
def add_question(id):

    # Permission checks
    qs = get_questionset(id)

    text = flask.request.form['text']
    r.rpush(q_key, text)

@questionset_api.route('/<id>/question/<index>', methods = ['DELETE'])
def remove_question(id, index):

    # Permission checks
    qs = get_questionset(id)

    text = flask.request.form['text']
    r.rpush(q_key, text)

    qsq_key = 'questionset:{id}:questions'.format(id = id)

    r.lset(qsq_key, index, '__DELETED__')
    r.lrem(qsq_key, '__DELETED__')

@questionset_api.route('/<id>/question/<index>', methods = ['POST'])
def modify_question(id, index):

    # Permission checks
    qs = get_questionset(id)

    text = flask.request.form['text']
    r.rpush(q_key, text)

    qsq_key = 'questionset:{id}:questions'.format(id = id)

    text = flask.request.form['text']
    r.lset(qsq_key, index, text)
