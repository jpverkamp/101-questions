import lib
import models

class Message(lib.RedisDict):
    '''A single message in a threaded conversation.'''

    def __init__(self, id = None, **defaults):

        lib.RedisDict.__init__(
            self,
            id = id,
            fields = {
                'author': models.User,
                'test': str,
                'date': str,
                'responses': lib.RedisList.as_child(self, 'questions', models.Message),
            },
            defaults = defaults
        )
