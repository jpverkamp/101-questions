import json
import lib
import math
import models
import flask

def register(app):

    @app.route('/questionset/<id>', defaults = {'page' : None})
    @app.route('/questionset/<id>/<int:page>')
    @lib.authenticated
    def get_questionset(id, page = None):

        user = lib.current_user()
        qs = models.QuestionSet(id)

        if page is None:
            page = math.floor(qs['current-question'] / 10) + 1

        total_pages = max(1, math.ceil(len(qs['questions']) / 10))

        # Not enough pages for pagination
        if total_pages == 1:
            pages = False
        # Otherwise generate a list with the first, last, and a range around the current
        else:
            pages = [1]

            if page > 4:
                pages += ['...']

            for i in range(page - 2, page + 3):
                if i > 1 and i < total_pages - 1:
                    pages += [i]

            if page < total_pages - 4:
                pages += ['...']

            pages += [total_pages]

        return flask.render_template(
            'questionset.html',
            user = user,
            questionset = qs,
            pages = pages,
            current_page = page,
            total_pages = total_pages,
        )

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
            if qs == each_qs:
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
        elif field == 'frequency': # Validate frequencies
            try:
                qs[field] = lib.Frequency(flask.request.form['value'])
            except:
                return 'Invalid frequency. Options:\n' + lib.Frequency.options_string(), 400
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

    @app.route('/questionset/<id>/toggle/<mode>', methods = ['POST'])
    @lib.authenticated
    def update_questionset_modes(id, mode):

        questionset = models.QuestionSet(id)

        state = flask.request.form['state']
        questionset['mode-{}'.format(mode)] = json.loads(state)

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

        # If the question deleted was before the current index, don't skip a question
        if index < qs['current-question']:
            qs['current-question'] -= 1

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
