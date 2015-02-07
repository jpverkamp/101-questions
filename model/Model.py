import json
import os
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

        self.doNotSave = False
        self.id = id
        self.path = os.path.join('data', self.__class__.__name__, self.id)
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

        if create:
            pass

        elif os.path.exists(self.path):
            print('Loading {path}'.format(path = self.path))
            with open(self.path, 'r') as fin:
                for k, v in json.load(fin).items():
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
          print('Saving {path}'.format(path = self.path))
          with open(self.path, 'w') as fout:
              json.dump(self, fout)

    def delete(self):
        '''Delete the object'''

        print('Deleting {path}'.format(path = self.path))
        os.remove(self.path)
        self.doNotSave = True
