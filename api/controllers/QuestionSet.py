from lib.RESTController import RESTController
from models import QuestionSet, Question

class QuestionSetController(RESTController):

    def __init__(self, app):
        RESTController.__init__(self,
            app,
            QuestionSet,
            visibleFields = ['title', 'questions'],
            mutableFields = ['title'],
            mutableListFields = [('questions', Question)]
        )
