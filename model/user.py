# -*- coding: utf-8 -*-

import base64
import bcrypt
import flask

import model.base

class User(model.base.BaseModel):

    def __init__(self, app, id = None, **kwargs):
        super(User, self).__init__(
            app,
            id,
            {
                'name': None,
                'email': None,
                'password': None,
            },
            True,
            **kwargs
        )

        # Special updates on new users
        if id == None:
            # Create self-admin permissions for each user
            self.setPermission(self, 'admin')

            # Store the email to id mapping
            app.redis.hset('email->user_id', self.data['email'], self.id)

    def __setitem__(self, key, val):

        super(User, self).__setitem__(key, val)

        # If we changed the email address, update the mapping
        if key == 'email':
            app.redis.hset('email->user_id', self['email'], self.id)

    def setPassword(self, password):
        '''Store a hashed password for a given user.'''

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        hashed = base64.b64encode(hashed).decode()

        self['password'] = hashed

    def verifyPassword(self, password):
        '''Verify that a user entered the correct password.'''

        hashed = self['password']
        if hashed:
            hashed = base64.b64decode(hashed)
            return bcrypt.hashpw(password.encode(), hashed) == hashed

    def hasPermission(self, other, mode):
        '''Does this user have access to the given object.'''

        if not self.app.checkPermissions or not other.auth:
            return True

        if self == other:
            return True

        permission = self.app.redis.hget(
            'permission:{user_id}'.format(user_id = self.id),
            '{resource_type}:{resource_id}'.format(
                resource_type = other.__class__.__name__,
                resource_id = other.id
            )
        )
        if permission:
            permission = permission.decode()

        return ((mode == 'read' and permission in ('read', 'write', 'admin'))
                or (mode == 'write' and permission in ('write', 'admin'))
                or (mode == 'admin' and permission in ('admin',)))

    def setPermission(self, other, mode):
        '''
        Set this user's permission to another object.

        Set mode to None to remove permissions entirely.
        '''

        hash_key = 'permission:{user_id}'.format(user_id = self.id)
        res_key = '{resource_type}:{resource_id}'.format(
            resource_type = other.__class__.__name__,
            resource_id = other.id
        )

        if mode:
            self.app.redis.hset(hash_key, res_key, mode)
        else:
            self.app.redis.delete(hash_key, res_key)

    def getResources(self, type = None, permission = None, id_only = False):
        '''
        Get all resources this user has permission for.

        If type is not specified, return all resources.

        If a permission is specified, only return items with a permission less
        than or equal to that (write will return or write but not admin).

        If id_only, generates a list of ids. Otherwise, generates a list of
        tuples of the form (type, id, permission)
        '''

        for item, item_permission in self.app.redis.hgetall('permission:{user_id}'.format(user_id = self.id)).items():
            item = item.decode()
            item_permission = item_permission.decode()

            if type and not item.startswith(type):
                continue

            if permission and (
                    (item_permission == 'read' and not permission in ('read' ,'write', 'admin'))
                    or (item_permission == 'write' and not permission in ('write', 'admin'))
                    or (item_permission == 'admin' and not permission in ('admin',))
                ):
                continue

            item_type, item_id = item.split(':', 1)
            if id_only:
                yield item_id
            else:
                yield (item_type, item_id, item_permission)

def byEmail(app, email):

    id = app.redis.hget('email->user_id', email)
    if id:
        return User(app, id)
    else:
        return None

def current(app):

    try:
        return app.user
    except:
        pass

    try:
        return User(app, flask.session['user_id'])
    except:
        pass

    return None
