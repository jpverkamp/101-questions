# -*- coding: utf-8 -*-

import copy
import flask
import json
import random

class BaseModel(object):
    '''Base model for redis backed objects, override this.'''

    ID_LENGTH = 13

    def __init__(self, app, id, template, auth, **kwargs):
        self.app = app
        self.auth = auth

        if id == None:
            format_str = '{0:0%sx}' % BaseModel.ID_LENGTH
            self.id = format_str.format(random.randrange(16 ** BaseModel.ID_LENGTH))
        else:
            self.id = id

        if not isinstance(self.id, str):
            self.id = self.id.decode()

        self.key = 'data:{name}:{resource_id}'.format(
            name = self.__class__.__name__,
            resource_id = self.id
        )

        new_data = False

        data = self.app.redis.get(self.key)
        if data:
            self.data = json.loads(data.decode())
        else:
            self.data = copy.deepcopy(template)
            new_data = True

        for k, v in kwargs.items():
            self.data[k] = v
            new_data = True

        # If we updated any data, write it out now
        if new_data:
            data = json.dumps(self.data)
            self.app.redis.set(self.key, data)

    def __getitem__(self, key):
        '''Load a value from redis, caching in local memory for multiple reads.'''

        if self.app.checkPermissions and self.auth:
            import model.user
            if not model.user.current(self.app).hasPermission(self, 'read'):
                return None

        if key in self.data:
            return self.data[key]
        else:
            return None

    def __setitem__(self, key, val):
        '''Save a value, automatically push to redis.'''

        if self.app.checkPermissions and self.auth:
            import model.user
            if not model.user.current(self.app).hasPermission(self, 'write'):
                return

        self.data[key] = val
        data = json.dumps(self.data)
        self.app.redis.set(self.key, data)
