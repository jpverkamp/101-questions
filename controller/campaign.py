# -*- coding: utf-8 -*-

import flask
import json

import model.campaign
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
