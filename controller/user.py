# -*- coding: utf-8 -*-

import json
import flask

import model.user

def register(app):

    @app.route('/api/v1/user', methods = ["POST"])
    def create_user():

        name = flask.request.form['name']
        email = flask.request.form['email']
        password = flask.request.form['password']

        # Check that the email is not currently in use
        if model.user.byEmail(app, email):
            flask.abort(400)

        new_user = model.user.User(app, name = name, email = email)

        if new_user:
            with app.unsafe():
                new_user.setPassword(password)

            return json.dumps(new_user.id)
        else:
            flask.abort(400)

    @app.route('/api/v1/user/me', methods = ["GET"])
    def user_me():
        '''Return information about the current user'''

        try:
            return user(model.user.current(app).id)
        except:
            return json.dumps({})


    @app.route('/api/v1/user/<id>', methods = ["GET"])
    def user(id):
        user = model.user.User(app, id)

        if user and user.data:
            user = user.data
            del user['password']
            return json.dumps(user)
        else:
            return json.dumps({})

    @app.route('/login', methods = ["POST"])
    def login():
        '''Log a user in'''

        email = flask.request.form['email']
        password = flask.request.form['password']

        with app.unsafe():
            user = model.user.byEmail(app, email)

            if user and user.verifyPassword(password):
                flask.session['user_id'] = user.id
                return user_me()

            flask.abort(400)
