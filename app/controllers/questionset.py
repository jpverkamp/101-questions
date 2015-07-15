import models
import lib
import flask

def register(app):

    @app.route('/questionset/<id>')
    @lib.authenticated
    def get_questionset(id):

        qs = models.QuestionSet(id)
        return flask.render_template('questionset.html', questionset = qs)

    @app.route('/questionset', methods = ['POST'])
    @lib.authenticated
    def create_questionset():

        user = lib.current_user()
        qs = models.QuestionSet()
        user['questionsets'].append(qs)

        return get_questionset(qs.id)
