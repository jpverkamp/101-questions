# -*- coding: utf-8 -*-

import flask
import json

import model.questionset
import model.user

def register(app):

    @app.route('/api/v1/questionset', methods = ["POST"])
    def create_questionset():

        title = flask.request.form['title']
        questions = flask.request.form['questions']

        user = model.user.current(app)
        if not user:
            flask.abort(400)

        with app.unsafe():
            new_qs = model.questionset.QuestionSet(
                app,
                title = title,
                questions = questions.split('\n')
            )

            user.setPermission(new_qs, 'admin')

        return json.dumps(new_qs.id)

    @app.route('/api/v1/questionsets/', methods = ["GET"])
    def all_questionsets():

        user = model.user.current(app)
        if user:
            return json.dumps(list(user.getResources(type = 'QuestionSet', id_only = True)))
        else:
            return json.dumps([])

    @app.route('/api/v1/questionset/<id>', methods = ["GET"])
    def get_questionset(id):

        qs = model.questionset.QuestionSet(app, id)
        if qs:
            return json.dumps(qs.data)
        else:
            return json.dumps({})
