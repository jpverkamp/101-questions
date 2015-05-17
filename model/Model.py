import codecs
import json
import os
import redis
import threading
import time
import utils

class Model(dict):

    def __init__(self, id = None, **data):
        '''
        Load/create a model.

        If id is None, create a new object.
        If id is not None, load that object from disk.

        If id is not None and the object doesn't exist, fail.
        '''

        create = not id

        if not id:
            id = utils.randomID()

        self.redis = redis.StrictRedis(host='redis', port=6379, db=0)

        self.doNotSave = False
        self.id = id
        self.key = os.path.join(self.__class__.__name__, self.id)

        if create:
            pass

        elif self.redis.exists(self.key):
            print('Loading {path}'.format(path = self.key))
            js = self.redis.get(self.key).decode("utf-8")
            for k, v in json.loads(js).items():
                self[k] = v

        else:
            raise Exception('Object does not exist')

        if data:
            for k, v in data.items():
                self[k] = v

        self['id'] = self.id

    def __del__(self):
        '''When the object in unloaded, save it to disk.'''

        if not self.doNotSave:
          print('Saving {path}'.format(path = self.key))
          js = json.dumps(self)
          self.redis.set(self.key, js)

    def delete(self):
        '''Delete the object'''

        print('Deleting {path}'.format(path = self.key))
        self.redis.delete(self.key)
        self.doNotSave = True

    @classmethod
    def listAllIDs(klass):
        '''Get all IDs for this kind of object.'''

        r = redis.StrictRedis(host='redis', port=6379, db=0)

        prefix = klass.__name__
        keys = [key.split('/')[-1] for key in r.keys(prefix + '*')]
        return keys
