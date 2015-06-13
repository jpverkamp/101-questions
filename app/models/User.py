import bcrypt

import lib
import models

class User(lib.RedisObject):
    '''A user. Duh.'''

    @classmethod
    def classinit(cls):
        cls.fields = {
            'name': str,
            'email': str, # This will actually be used as ID # TODO: clean this behavior up somehow
            'password': str,
        }

        cls.lists = {
            'friends': models.User,
            'pending-friends': models.User,
            'questionsets': models.QuestionSet
        }

    def __init__(self, id = None, email = None, **kwargs):

        # Use either id or email if specified, error if both
        if id and email:
            raise Exception('Do not specify both id and email for a user, they are the same thing')

        # If 'me' is specified as the user, get the current user and use that
        if id == 'me' or email == 'me':
            id = lib.utils.current_user()['email']

        lib.RedisObject.__init__(self, id = (id if id else email), **kwargs)

    def __getitem__(self, key):
        '''Override the behavior for email, since that is actually the id.'''

        if key == 'email':
            return self.id
        else:
            return lib.RedisObject.__getitem__(self, key)

    def __setitem__(self, key, val):
        '''Override the behavior if user is trying to change the password'''

        if key == 'password':
            password = bcrypt.hashpw(
                val.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            lib.RedisObject.__setitem__(self, 'password', password)

        else:

            lib.RedisObject.__setitem__(self, key, val)

    def verifyPassword(self, testPassword):
        '''Verify if a given password is correct'''

        hashedTestPassword = bcrypt.hashpw(
            testPassword.encode('utf-8'),
            self['password'].encode('utf-8')
        ).decode('utf-8')

        return hashedTestPassword == self['password']
