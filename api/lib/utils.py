import flask
import functools

from flask.ext.api import status

import models

def logged_in(f):
    '''Require that the user be logged in for this session'''

    @functools.wraps(f)
    def new_f(*args, **kwargs):
        # There is no user logged in
        if not 'id' in flask.session:
            flask.abort(status.HTTP_401_UNAUTHORIZED, 'Not logged in')

        # There is a user logged in, but they do not exist
        if not models.User(flask.session['id']):
            flask.abort(status.HTTP_404_NOT_FOUND, 'Logged in user not found')

        return f(*args, **kwargs)

    return new_f

@logged_in
def current_user():
    return models.User(flask.session['id'])

class renamed(object):
    '''Decorator to rename functions; used with Flask's name based routing'''

    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        @functools.wraps(f)
        def new_f(*args, **kwargs):
            return f(*args, **kwargs)

        new_f.__name__ = self.name
        return new_f
