from lib.RESTController import RESTController
from models import User, QuestionSet

class UserController(RESTController):

    def __init__(self, app):
        RESTController.__init__(self,
            app,
            User,
            visibleFields = ['name', 'questionsets'],
            mutableFields = ['name'],
            mutableListFields = [('questionsets', QuestionSet)]
        )
