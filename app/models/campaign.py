import lib
import models

class Campaign(lib.RedisDict):
    '''A set of questions currently being asked.'''

    def __init__(self, id = None, **defaults):

        lib.RedisDict.__init__(
            self,
            id = id,
            fields = {
                'targets': lib.RedisList.as_child(self, 'targets', models.User),
                'start-date': str,
                'frequency': str,
                'messages': lib.RedisList.as_child(self, 'messages', models.Message),
            },
            defaults = defaults
        )
