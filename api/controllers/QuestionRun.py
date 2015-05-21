from lib.RESTController import RESTController
from models import QuestionRun, User, AnsweredQuestion

class QuestionRunController(RESTController):

    def __init__(self, app):
        RESTController.__init__(self,
            app,
            QuestionRun,
            visibleFields = ['title', 'start_date', 'frequency', 'users', 'questions'],
            mutableFields = ['title', 'frequency'],
            mutableListFields = [('users', User), ('questions', AnsweredQuestion)]
        )
