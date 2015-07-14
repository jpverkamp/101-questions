import bcrypt

import lib
import models
import utils

class User(lib.RedisDict):
    '''A user. Duh.'''

    def __init__(self, id = None, email = None, **defaults):

        # Use either id or email if specified, error if both
        if id and email:
            raise Exception('Do not specify both id and email for a user, they are the same thing')

        # If 'me' is specified as the user, get the current user and use that
        if id == 'me' or email == 'me':
            id = utils.current_user()['email']

        # Set id and email to the same value
        id = id if id else email
        defaults['email'] = id

        lib.RedisDict.__init__(
            self,
            id = (id if id else email),
            fields = {
                'name': str,
                'email': str,
                'password': str,
                'friends': lib.RedisList.as_child(self, 'friends', models.User),
                'campaigns': lib.RedisList.as_child(self, 'campaigns', models.Campaign),
                'questionsets': lib.RedisList.as_child(self, 'questionsets', models.QuestionSet),
            },
            defaults = defaults
        )

    def __setitem__(self, key, val):
        '''Override the behavior if user is trying to change the password'''

        if key == 'password':
            val = bcrypt.hashpw(
                val.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

        lib.RedisDict.__setitem__(self, key, val)

    def verifyPassword(self, testPassword):
        '''Verify if a given password is correct'''

        hashedTestPassword = bcrypt.hashpw(
            testPassword.encode('utf-8'),
            self['password'].encode('utf-8')
        ).decode('utf-8')

        return hashedTestPassword == self['password']
