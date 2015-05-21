from lib.RESTController import RESTController
from models import AnsweredQuestion, Answer

class AnsweredQuestionController(RESTController):

    def __init__(self, app):
        RESTController.__init__(self,
            app,
            AnsweredQuestion,
            visibleFields = ['question', 'answers'],
            mutableFields = ['question'],
            mutableListFields = [('answers', Answer)]
        )
