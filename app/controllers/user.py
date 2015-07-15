import models
import lib
import flask

def register(app):

    @app.route('/user', defaults = {'email': 'me'})
    @app.route('/user/<email>', methods = ['GET'])
    @lib.authenticated
    def user(email):

        if email == 'me':
            email = flask.session['email']

        user = models.User(email)
        if user:
            return flask.render_template('user.html', user = user)
        else:
            flask.flash('User doesn\'t exist')
            return flask.render_template('/')
