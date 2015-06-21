import bcrypt
import flask
import json

import models

from utils import *
from controllers.flaskrest import make_blueprint

user_api = make_blueprint(
    models.User,
    lists = {
        'friends': models.User,
        'questionsets': models.QuestionSet
    }
)


@user_api.route('/login', methods = ['POST'])
def login():
    '''Login a user'''

    id = flask.request.form['email']
    password = flask.request.form['password']

    user = models.User(id)

    if not user:
        flask.abort(404, 'User not found')

    if not user.verifyPassword(password):
        flask.abort(403, 'Invalid password')

    flask.session['id'] = user['id']

    return json.dumps(True)

@user_api.route('/logout', methods = ['POST'])
def logout():
    '''Logout a user'''

    if 'id' in flask.session:
        del flask.session['id']

    return json.dumps(True)
