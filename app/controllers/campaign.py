import json
import lib
import models
import flask

def register(app):

    @app.route('/campaign/<id>')
    @lib.authenticated
    def get_campaign(id):

        user = lib.current_user()
        campaign = models.Campaign(id)
        return flask.render_template('campaign.html', user = user, campaign = campaign)

    @app.route('/campaign', methods = ['POST'])
    @lib.authenticated
    def create_campaign():

        user = lib.current_user()
        campaign = models.Campaign()
        user['campaigns'].append(campaign)

        return get_campaign(campaign.id)

    @app.route('/campaign/<id>/targets', methods = ['POST'])
    @lib.authenticated
    def update_campaign_targets(id):

        campaign = models.Campaign(id)
        target = models.User(flask.request.form['value'])
        state = json.loads(flask.request.form['state'])

        if state:
            campaign['targets'].append(target)
        else:
            for index, user in enumerate(campaign['targets']):
                if user == target:
                    del campaign['targets'][index]
                    break

        return json.dumps(True)

    @app.route('/campaign/<id>/<field>', methods = ['POST'])
    @lib.authenticated
    def update_campaign(id, field):

        if not field in ['title', 'start-date', 'frequency']:
            raise Exception('Unknown field: {}'.format(field))

        campaign = models.Campaign(id)
        campaign[field] = flask.request.form['value']
        return json.dumps(True)
