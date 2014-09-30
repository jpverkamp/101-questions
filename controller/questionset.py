# -*- coding: utf-8 -*-

import json

import model.questionset
import model.user

def register(app):

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
