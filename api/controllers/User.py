from lib.RESTController import RESTController
from models.User import User

class UserController(RESTController):

    def __init__(self, app):
        RESTController.__init__(self,
            app,
            User,
            visibleFields = ['name', 'questions'],
            mutableFields = ['name'],
            mutableListFields = ['name']
        )
