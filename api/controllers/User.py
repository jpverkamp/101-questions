import bcrypt
import flask
import json

from flask.ext.api import status

import utils

user_api = flask.Blueprint('user_api', __name__, url_prefix='/api/user')

# user:<email> is user data
# user:<email>:questionsets is a list of questionsets for a user

@user_api.route('/', methods = ['GET'])
def get_current_user():
    '''Get the current user if logged in'''

    if not 'email' in flask.session:
        flask.abort(status.HTTP_401_UNAUTHORIZED, 'Not logged in')

    email = flask.session['email']
    u_key = 'user:{email}'.format(email = email)
    uqs_key = 'user:{email}:questionsets'.format(email = email)

    r = utils.redis()

    user = r.hgetall(u_key)
    user['questionset-count'] = r.llen(uqs_key)

    del user['password']

    return json.dumps(user)

@user_api.route('/', methods = ['PUT'])
def create_user():
    '''Create a new user if a user with that email doesn't already exist'''

    logout()

    r = utils.redis()

    email = flask.request.form['email']
    name = flask.request.form['name']
    password = flask.request.form['password']

    u_key = 'user:' + email

    if r.exists(u_key):
        flask.abort(status.HTTP_409_CONFLICT, 'Email already exists')

    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    r.hset(u_key, 'name', name)
    r.hset(u_key, 'password', password_hash)

    return json.dumps(True)

@user_api.route('/', methods = ['POST'])
def change_user_fields():
    '''
    Change information about the user.

    name - change the name of the logged in user
    old-password and new-password - update password of the logged in user to new if old matches
    '''

    if not 'email' in flask.session:
        flask.abort(status.HTTP_401_UNAUTHORIZED, 'Not logged in')

    email = flask.session['email']
    u_key = 'user:' + email

    if not r.exists(u_key):
        flask.abort(status.HTTP_404_NOT_FOUND, 'User not found')

    if 'name' in flask.request.form:

        r.hset(u_key, 'name', name)

    if 'old-password' in flask.request.form and 'new-password' in flask.request.form:

        old_password = flask.request.form['old-password']
        new_password = flask.request.form['new-password']

        old_password_hash = r.hget('user:' + email)
        if not (old_password_hash == bcrypt.hashpw(
            old_password.encode('utf-8'),
            old_password_hash.encode('utf-8')
        ).decode('utf-8')):
            flask.abort(status.HTTP_403_FORBIDDEN, 'Invalid password')

        new_password_hash = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        r.hset(u_key, 'password', new_password_hash)

    return json.dumps(True)

@user_api.route('/login', methods = ['POST'])
def login():
    '''Login a user'''

    r = utils.redis()

    email = flask.request.form['email']
    password = flask.request.form['password']

    u_key = 'user:' + email

    if not r.exists(u_key):
        flask.abort(status.HTTP_404_NOT_FOUND, 'User not found')

    real_password_hash = r.hget(u_key, 'password')
    test_password_hash = bcrypt.hashpw(password.encode('utf-8'), real_password_hash.encode('utf-8')).decode('utf-8')

    if real_password_hash != test_password_hash:
        flask.abort(status.HTTP_403_FORBIDDEN, 'Invalid password')

    flask.session['email'] = email

    return json.dumps(True)

@user_api.route('/logout', methods = ['POST'])
def logout():
    '''Logout a user'''

    if 'email' in flask.session:
        del flask.session['email']

    return json.dumps(True)
