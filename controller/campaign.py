# -*- coding: utf-8 -*-

import flask
import json

import model.campaign
import model.questionset
import model.user

def register(app):

    @app.route('/api/v1/campaign', methods = ["POST"])
    def create_campaign():

        title = flask.request.form['title']
        start_date = flask.request.form['start_date']
        frequency = flask.request.form['frequency']

        user = model.user.current(app)
        if not user:
            flask.abort(400)

        users = [user.id]
        questions = []

        with app.unsafe():
            new_c = model.campaign.Campaign(
                app,
                title = title,
                start_date = start_date,
                frequency = frequency,
                users = users,
                questions = questions
            )

            user.setPermission(new_c, 'admin')

        return json.dumps(new_c.id)

    @app.route('/api/v1/campaigns/', methods = ["GET"])
    def all_campaigns():

        user = model.user.current(app)
        if user:
            return json.dumps(list(user.getResources(type = 'Campaign', id_only = True)))
        else:
            return json.dumps([])

    @app.route('/api/v1/campaign/<id>', methods = ["GET"])
    def get_campaign(id):

        c = model.campaign.Campaign(app, id)
        if c:
            return json.dumps(dict(c))
        else:
            return json.dumps({})

    @app.route('/api/v1/campaign/<id>', methods = ["PUT"])
    def update_campaign(id):

        c = model.campaign.Campaign(app, id)

        for basic_field in ['title', 'start_date', 'frequency']:
            if basic_field in flask.request.form:
                c[basic_field] = flask.request.form[basic_field]

        if 'questions' in flask.request.form:
            try:

                questions = []
                for line in flask.request.form['questions'].split('\n'):
                    qs_id, q_num = line.split('.')

                    # Validate that the question set exists and is readable
                    qs = model.questionset.QuestionSet(app, qs_id)

                    # Validate the the question exists in the questionset
                    q_num = int(q_num)
                    if q_num < 0 or q_num >= len(qs['questions']):
                        flask.abort(400)

                    questions.append([qs_id, q_num])

                c['questions'] = questions

            except:
                flask.abort(400)

        return json.dumps(dict(c))
