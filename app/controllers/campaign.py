import json
import lib
import models
import flask

def register(app):

    @app.route('/campaign/<id>')
    @lib.authenticated
    def get_campaign(id):

        c = models.Campaign(id)
        return flask.render_template('campaign.html', campaign = c)

    @app.route('/campaign', methods = ['POST'])
    @lib.authenticated
    def create_campaign():

        user = lib.current_user()
        c = models.Campaign()
        user['campaigns'].append(c)

        return get_campaign(c.id)

    @app.route('/campaign/<id>/<field>', methods = ['POST'])
    @lib.authenticated
    def update_campaign(id, field):

        if not field in ['title', 'start-date', 'frequency']:
            raise Exception('Unknown field: {}'.format(field))

        c = models.Campaign(id)
        c[field] = flask.request.form['value']
        return json.dumps(True)
