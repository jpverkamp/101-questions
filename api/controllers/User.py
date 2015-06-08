import bcrypt
import flask
import json

from flask.ext.api import status

import models

from lib.utils import *
from lib import make_blueprint

user_api = make_blueprint(models.User)

@user_api.route('/login', methods = ['POST'])
def login():
    '''Login a user'''

    id = flask.request.form['email']
    password = flask.request.form['password']

    user = models.User(id)

    if not user:
        flask.abort(status.HTTP_404_NOT_FOUND, 'User not found')

    if not user.verifyPassword(password):
        flask.abort(status.HTTP_403_FORBIDDEN, 'Invalid password')

    flask.session['id'] = user['id']

    return json.dumps(True)

@user_api.route('/logout', methods = ['POST'])
def logout():
    '''Logout a user'''

    if 'id' in flask.session:
        del flask.session['id']

    return json.dumps(True)
