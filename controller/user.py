# -*- coding: utf-8 -*-

import json
import flask

import model.user

def register(app):

    @app.route('/api/v1/user/login', methods = ["POST"])
    def user_login():
        '''Log a user in'''

        email = flask.request.form['email']
        password = flask.request.form['password']

        app.checkPermissions = False
        user = model.user.byEmail(app, email)
        logged_in = False

        if user and user.verifyPassword(password):
            flask.session['user_id'] = user.id
            logged_in = True

        app.checkPermissions = True
        return json.dumps(logged_in)

    @app.route('/api/v1/user/<id>', methods = ["GET"])
    def user(id):
        user = model.user.User(app, id)

        if user and user.data:
            user = user.data
            del user['password']
            return json.dumps(user)
        else:
            return json.dumps({})

    @app.route('/api/v1/user/me', methods = ["GET"])
    def user_me():
        '''Return information about the current user'''

        try:
            return user(model.user.current(app).id)
        except:
            return json.dumps({})

    @app.route('/api/v1/user/register', methods = ["POST"])
    def create_user():
        pass
