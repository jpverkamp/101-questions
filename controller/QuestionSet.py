import datetime
import flask
import json

from model.QuestionSet import QuestionSet

def init(app):

    SINGULAR_FIELDS = ['title', 'frequency']
    PLURAL_FIELDS = ['email', 'question']

    @app.route('/questionset', methods = ['post'])
    def createQuestionSet():
        return json.dumps(QuestionSet(
            id = None,
            title = flask.request.form['title'],
            frequency = flask.request.form['frequency'],
            emails = [flask.request.form['email']],
            questions = [],
            nextQuestion = 0,
            lastSent = datetime.datetime.now().timestamp()
        ))

    @app.route('/questionset/<id>', methods = ['get'])
    def getQuestionSet(id):
        return json.dumps(QuestionSet(id))

    @app.route('/questionset/<id>/<field>', methods = ['get'])
    def getQuestionSetSingularField(id, field):
        return json.dumps(QuestionSet(id)[field])

    @app.route('/questionset/<id>/<field>/<int:field_id>', methods = ['get'])
    def getQuestionSetPluralField(id, field, field_id):
        return json.dumps(QuestionSet(id)[field + 's'][field_id])

    @app.route('/questionset/<id>/send-next', methods = ['post'])
    def forceSendNext(id):
        qs = QuestionSet(id)
        qs.sendNext()
        return json.dumps(qs)

    @app.route('/questionset/<id>/<field>', methods = ['post'])
    def addToQuestionSetPluralField(id, field):
        qs = QuestionSet(id)

        if flask.request.form[field].startswith('['):
            for each in json.loads(flask.request.form[field]):
                qs[field].append(each)
        else:
            qs[field + 's'].append(flask.request.form[field])

        return json.dumps(qs)

    @app.route('/questionset/<id>/<field>', methods = ['put'])
    def overwriteQuestionSetSingularField(id, field):
        qs = QuestionSet(id)
        if flask.request.form[field].startswith('['):
            qs[field] = json.loads(flask.request.form[field])
        else:
            qs[field] = flask.request.form[field]
        return json.dumps(qs)

    @app.route('/questionset/<id>/<field>/<int:field_id>', methods = ['put'])
    def overwriteQuestionSetPluralField(id, field, field_id):
        qs = QuestionSet(id)
        qs[field + 's'][field_id] = flask.request.form[field]
        return json.dumps(qs)

    @app.route('/questionset/<id>', methods = ['delete'])
    def deleteFromQuestionSet(id):
        return json.dumps(QuestionSet(id).delete())

    @app.route('/questionset/<id>/<field>/<int:field_id>', methods = ['delete'])
    def removeQuestionSetField(id, field, field_id):
        qs = QuestionSet(id)

        # If deleting a question that's already been asked, move the indicator back
        if field == 'question' and field_id < qs['nextQuestion']:
            qs['nextQuestion'] -= 1

        del qs[field + 's'][field_id]
        return json.dumps(qs)
