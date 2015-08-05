import json
import lib
import models
import flask

def register(app):

    @app.route('/questionset/<id>')
    @lib.authenticated
    def get_questionset(id):

        user = lib.current_user()
        qs = models.QuestionSet(id)
        return flask.render_template('questionset.html', user = user, questionset = qs)

    @app.route('/questionset', methods = ['POST'])
    @lib.authenticated
    def create_questionset():

        user = lib.current_user()
        qs = models.QuestionSet()
        user['questionsets'].append(qs)

        return get_questionset(qs.id)

    @app.route('/questionset/<id>', methods = ['DELETE'])
    @lib.authenticated
    def delete_questionset(id):

        user = lib.current_user()
        qs = models.QuestionSet(id)

        for index, each_qs in enumerate(user['questionsets']):
            print('Trying {} vs {}'.format(qs, each_qs))
            if qs == each_qs:
                print('GOT IT!')
                del user['questionsets'][index]
                break

        qs.delete()

        return json.dumps(True)

    @app.route('/questionset/<id>/<field>', methods = ['POST'])
    @lib.authenticated
    def update_questionset(id, field):

        qs = models.QuestionSet(id)

        if field == 'current-question': # Questions are zero indexed internally
            qs[field] = int(flask.request.form['value']) - 1
        else:
            qs[field] = flask.request.form['value']

        return json.dumps(True)

    @app.route('/questionset/<id>/questions', methods = ['POST'])
    @lib.authenticated
    def add_question_to_questionset(id):

        qs = models.QuestionSet(id)
        qs['questions'].append('')
        return json.dumps(True)

    @app.route('/questionset/<id>/targets', methods = ['POST'])
    @lib.authenticated
    def update_questionset_targets(id):

        questionset = models.QuestionSet(id)
        target = models.User(flask.request.form['value'])
        state = json.loads(flask.request.form['state'])

        if state:
            questionset['targets'].append(target)
        else:
            for index, user in enumerate(questionset['targets']):
                if user == target:
                    del questionset['targets'][index]
                    break

        return json.dumps(True)

    @app.route('/questionset/<id>/cron-hour', methods = ['POST'])
    @lib.authenticated
    def update_questionset_cron_hour(id):

        qs = models.QuestionSet(id)
        qs['cron-hour'] = int(flask.request.form['value'])
        return json.dumps(True)

    @app.route('/questionset/<id>/questions/<int:index>', methods = ['POST'])
    @lib.authenticated
    def update_question_in_questionset(id, index):

        qs = models.QuestionSet(id)
        qs['questions'][index] = flask.request.form['value']
        return json.dumps(True)

    @app.route('/questionset/<id>/questions/<int:index>', methods = ['DELETE'])
    @lib.authenticated
    def delete_question_from_questionset(id, index):

        qs = models.QuestionSet(id)
        del qs['questions'][index]
        return json.dumps(True)

    @app.route('/questionset/<id>/questions/send-next', methods = ['POST'])
    @lib.authenticated
    def send_next_question_from_questionset(id):

        qs = models.QuestionSet(id)
        qs.send_next()
        return json.dumps(True)

    @app.route('/questionset/<id>/questions/import', methods = ['GET'])
    @lib.authenticated
    def display_questionset_import(id):

        qs = models.QuestionSet(id)
        return flask.render_template(
            'import.html',
            redirect = '/questionset/{id}'.format(id = id),
            action = '/questionset/{id}/questions/import'.format(id = id),
            type = 'Question Set "{title}"'.format(title = qs['title'])
        )

    @app.route('/questionset/<id>/questions/import', methods = ['POST'])
    @lib.authenticated
    def questionset_import(id):

        qs = models.QuestionSet(id)

        raw_values = flask.request.form['values']
        try:
            values = json.loads(raw_values)
        except:
            values = raw_values.split('\n')

        for value in values:
            qs['questions'].append(value)

        if 'redirect' in flask.request.form and flask.request.form['redirect']:
            return flask.redirect(flask.request.form['redirect'])
        else:
            return flask.redirect('/')
