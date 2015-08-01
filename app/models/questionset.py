import lib
import models

class QuestionSet(lib.RedisDict):
    '''A list of questions that can be combined into a campaign.'''

    def __init__(self, id = None, **defaults):

        lib.RedisDict.__init__(
            self,
            id = id,
            fields = {
                'title': str,
                'frequency': str,
                'targets': lib.RedisList.as_child(self, 'targets', models.User),
                'next-question': str,
                'questions': lib.RedisList.as_child(self, 'questions', str),
            },
            defaults = defaults
        )
