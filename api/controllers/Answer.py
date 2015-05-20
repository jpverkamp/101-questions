from lib.RESTController import RESTController
from models import Answer

class AnswerController(RESTController):

    def __init__(self, app):
        RESTController.__init__(self,
            app,
            Answer,
            visibleFields = ['text'],
            mutableFields = ['text'],
        )
