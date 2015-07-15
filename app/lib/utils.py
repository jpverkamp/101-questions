import flask
import functools
import models

def current_user():
    if 'email' in flask.session:
        return models.User(flask.session['email'])

def authenticated(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        if current_user():
            return f(*args, **kwargs)
        else:
            flask.abort(403)

    return inner
