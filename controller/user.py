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

    @app.route('/api/v1/user/<id>', methods = ["GET"])
    def get_user(id):
        if id == 'me':
            try:
                id = model.user.current(app).id
            except:
                return json.dumps({})

        user = model.user.User(app, id)
        user_data = dict(user)

        if user_data:
            del user_data['password']
            return json.dumps(user_data)
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
                return get_user('me')

            flask.abort(400)
