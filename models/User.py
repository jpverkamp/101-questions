from models.RedisObject import RedisObject

import bcrypt

class User(RedisObject):
    def __init__(self, name, email, password):
        RedisObject.__init__(self,
            name = name,
            id = email,
            questionsets = [],
            friends = []
        )

        # This needs to be here to trigger __setitem__ below
        self[password] = password

    def __setitem__(self, key, val):
        if key == 'password':
            val = bcrypt.hashpw(
                val.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

        RedisObject.__setitem__(self, key, val)

    def verifyPassword(self, password):

        hashed = self['password']
        password = bcrypt.hashpw(
            password.encode('utf-8'),
            hashed.encode('utf-8')
        ).decode('utf-8')

        return hashed == password
