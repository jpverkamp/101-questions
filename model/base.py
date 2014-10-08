# -*- coding: utf-8 -*-

import copy
import flask
import functools
import json
import random

def check_permission(which, self = None):
    '''Check permission for this object'''

    # Do the actual permission check against a given object
    # Bail out on the connection completely if the check fails
    def check(obj):
        if obj.app.checkPermissions and obj.auth:

            import model.user

            with obj.app.unsafe(): # Don't check permissions in permission check
                current_user = model.user.current(obj.app)

            if not (current_user and current_user.hasPermission(obj, which)):
                flask.abort(400)

    # If self is passed, we are not a decorator, check directly
    if self:
        check(self)

    # Otherwise, we're being called as a decorator
    else:
        def wrapper(f):

            @functools.wraps(f)
            def new_f(self, *args, **kwargs):
                check(self)
                return f(self, *args, **kwargs)

            return new_f

        return wrapper

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
        data = self.app.redis.get(self.key)

        new_data = False

        if data:
            check_permission('read', self)
            self.data = json.loads(data.decode())
        elif not id:
            self.data = copy.deepcopy(template)
            new_data = True
        else:
            self.data = {}

        for k, v in kwargs.items():
            self.data[k] = v
            new_data = True

        # If we updated any data, write it out now
        if new_data:
            data = json.dumps(self.data)
            self.app.redis.set(self.key, data)

    @check_permission('read')
    def __getitem__(self, key):
        '''Load a value from redis, caching in local memory for multiple reads.'''

        if key in self.data:
            return self.data[key]
        else:
            return None

    @check_permission('write')
    def __setitem__(self, key, val):
        '''Save a value, automatically push to redis.'''

        self.data[key] = val
        data = json.dumps(self.data)
        self.app.redis.set(self.key, data)

    @check_permission('read')
    def __iter__(self):
        '''Allow iteration over objects and direct conversion with dict(...)'''

        for key in self.data:
            yield key, self.data[key]

    def __str__(self):
        '''Simple string representation'''

        return '{0}:{1}'.format(self.__class__.__name__, self.id)

    def __repr__(self):
        '''More detailed string representation'''

        with self.app.unsafe():
            return '{0}:{1}={2}'.format(self.__class__.__name__, self.id, dict(self))
