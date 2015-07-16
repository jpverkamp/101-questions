import json
import lib
import models
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

    @app.route('/questionset/<id>/title', methods = ['POST'])
    @lib.authenticated
    def update_questionset(id):

        qs = models.QuestionSet(id)
        qs['title'] = flask.request.form['value']
        return json.dumps(True)

    @app.route('/questionset/<id>/questions', methods = ['POST'])
    @lib.authenticated
    def add_question_to_questionset(id):

        qs = models.QuestionSet(id)
        qs['questions'].append('')
        return json.dumps(True)

    @app.route('/questionset/<id>/questions/<int:index>', methods = ['POST'])
    @lib.authenticated
    def update_question_in_questionset(id, index):

        qs = models.QuestionSet(id)
        qs['questions'][index] = flask.request.form['value']
        return json.dumps(True)
