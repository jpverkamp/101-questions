import flask
import functools
import models
import threading

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

def daemonize(f):
    '''Run the wrapped function as a daemon thread, starting immediately.'''

    f._thread = threading.Thread(target = f)
    f._thread.daemon = True
    f._thread.start()

    return f
