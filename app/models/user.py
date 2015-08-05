import bcrypt
import hashlib
import hmac
import lib
import models
import utils
import os
import sys

if not 'HMAC_KEY' in os.environ:
    print('ENV missing: HMAC_KEY')
    sys.exit(0)

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
        if defaults:
            defaults['email'] = id

        lib.RedisDict.__init__(
            self,
            id = (id if id else email),
            fields = {
                'name': str,
                'email': str,
                'password': str,
                'friends': lib.RedisList.as_child(self, 'friends', models.User),
                'questionsets': lib.RedisList.as_child(self, 'questionsets', models.QuestionSet),
            },
            defaults = defaults
        )

    def __bool__(self):
        '''Must have name set, not just email'''

        return lib.RedisDict.__bool__(self) and bool(self['name'])


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

    def generateFriendship(self, target_email):
        '''Generate a potential friendship link from this user to another.'''

        params = 'src={me}&dst={them}'.format(me = self['email'], them = target_email)
        signature = hmac.new(
            os.environ['HMAC_KEY'].encode('utf-8'),
            params.encode('utf-8'),
            digestmod = hashlib.sha256
        ).hexdigest()

        return '/friendship/verify?{params}&sig={signature}'.format(params = params, signature = signature)

    def verifyFriendship(self, params):
        '''
        Verify that we sent the previous friendship link.

        If we did, create a friendship between the two users.
        '''

        if params['dst'] != self['email']:
            raise Exception('Friendship link not sent to current user')

        paramstring = 'src={src}&dst={dst}'.format(src = params['src'], dst = params['dst'])
        signature = hmac.new(
            os.environ['HMAC_KEY'].encode('utf-8'),
            paramstring.encode('utf-8'),
            digestmod = hashlib.sha256
        ).hexdigest()

        if signature != params['sig']:
            raise Exception('Friendship signature not valid')

        other = models.User(params['src'])

        self['friends'].append(other)
        other['friends'].append(self)

        return True
