import models

class QuestionSet(models.RedisDict):
    '''A list of questions that are or have been sent.'''

    def __init__(self, id = None, **defaults):

        models.RedisDict.__init__(
            self,
            id = id,
            fields = {
                'title': str,
                'start-date': str,
                'frequency': str,
                'current-question': int,
                'recipients': models.RedisList.as_child(self, 'recipients', models.User),
                'questions': models.RedisList.as_child(self, 'questions', str),
            },
            defaults = defaults
        )
