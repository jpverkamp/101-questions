from lib import RedisObject

import models

class QuestionSet(RedisObject):
    '''A list of questions that are or have been sent.'''

    @classmethod
    def classinit(cls):
        cls.fields = {
            'owner': models.User,
            'title': str,
            'startDate': str,
            'frequency': str,
            'currentQuestion': int,
        }

        cls.lists = {
            'recipients': models.User,
            'questions': str,
        }

    def __init__(self, id = None, **kwargs):
        lib.RedisObject.__init__(self, id = id, **kwargs)
