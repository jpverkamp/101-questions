import bcrypt
import flask
import json
import redis

user_api = flask.Blueprint('user_api', __name__, url_prefix='/api/user')

@user_api.route('/', methods = ['PUT'])
def create_user():
    '''Create a new user if a user with that email doesn't already exist'''

    r = redis.StrictRedis(host = 'redis')

    email = flask.request.form['email']
    name = flask.request.form['name']
    password = flask.request.form['password']

    rkey = 'user:' + email

    if r.exists(rkey):
        flask.abort(409, msg = 'Email already exists')

    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    r.hset(rkey, 'name', name)
    r.hset(rkey, 'password', password_hash)

@user_api.route('/', methods = ['POST'])
def change_user_fields():
    '''
    Change information about the user.

    name - change the name of the logged in user
    old-password and new-password - update password of the logged in user to new if old matches
    '''

    if not 'email' in flask.session:
        flask.abort(401, 'Not logged in')

    email = flask.session['email']
    rkey = 'user:' + email

    if not r.exists(rkey):
        flask.abort(404, msg = 'User not found')

    if 'name' in flask.request.form:

        r.hset(rkey, 'name', name)

    if 'old-password' in flask.request.form and 'new-password' in flask.request.form:

        old_password = flask.request.form['old-password']
        new_password = flask.request.form['new-password']

        old_password_hash = r.hget('user:' + email)
        if not (old_password_hash == bcrypt.hashpw(
            old_password.encode('utf-8'),
            old_password_hash.encode('utf-8')
        ).decode('utf-8')):
            flask.abort(403, msg = 'Invalid password')


        new_password_hash = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        r.hset(rkey, 'password', new_password_hash)

@user_api.route('/login', methods = ['POST'])
def login():
    '''Login a user'''

    r = redis.StrictRedis(host = 'redis')

    email = flask.request.form['email']
    password = flask.request.form['password']

    if not r.exists(email):
        flask.abort(404, msg = 'User not found')

    rkey = 'user:' + email

    password_hash = r.hget('user:' + email)
    if not (password_hash == bcrypt.hashpw(
        password.encode('utf-8'),
        password_hash.encode('utf-8')
    ).decode('utf-8')):
        flask.abort(403, msg = 'Invalid password')

    flask.session['email'] = email

@user_api.route('/logout', methods = ['POST'])
def logout():
    '''Logout a user'''

    del flask.session['current_user']
