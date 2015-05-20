from lib.RESTController import RESTController
from models import Question

class QuestionController(RESTController):

    def __init__(self, app):
        RESTController.__init__(self,
            app,
            Question,
            visibleFields = ['text'],
            mutableFields = ['text'],
        )
