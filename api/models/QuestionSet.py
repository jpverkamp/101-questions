import lib
import models

class QuestionSet(lib.RedisObject):
    '''A list of questions that are or have been sent.'''

    @classmethod
    def classinit(cls):
        cls.fields = {
            'title': str,
            'start-date': str,
            'frequency': str,
            'current-question': int,
        }

        cls.lists = {
            'recipients': models.User,
            'questions': str,
        }

    def __init__(self, id = None, **kwargs):
        lib.RedisObject.__init__(self, id = id, **kwargs)
