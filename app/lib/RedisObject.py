import base64
import json
import redis
import os

class RedisObject(object):
    '''
    A base object backed by redis.

    Genrally, use RedisDict or RedisList rather than this directly.
    '''

    def __init__(self, id = None):
        '''Create or load a RedisObject.'''

        self.redis = redis.StrictRedis(host = 'redis', decode_responses = True)

        if id:
            self.id = id
        else:
            self.id = base64.urlsafe_b64encode(os.urandom(9)).decode('utf-8')

        if ':' not in self.id:
            self.id = self.__class__.__name__ + ':' + self.id

    def __bool__(self):
        '''Test if an object currently exists'''

        return self.redis.exists(self.id)

    def __eq__(self, other):
        '''Tests if two redis objects are equal (they have the same key)'''

        return self.id == other.id

    def __str__(self):
        '''Return this object as a string for testing purposes.'''

        return self.id

    def __repr__(self):
        '''TODO: FIX'''

        return str(self)

    @classmethod
    def all(cls):
        '''Iterate through all objects of the given class.'''

        r = redis.StrictRedis(host = 'redis', decode_responses = True)

        for key in r.keys(cls.__name__ + ':*'):
            if key.count(':') == 1:
                yield cls(key)

    def delete(self):
        '''Delete this object from redis'''

        self.redis.delete(self.id)

    @staticmethod
    def decode_value(type, value):
        '''Decode a value if it is non-None, otherwise, decode with no arguments.'''

        if value == None:
            try:
                return type()
            except:
                return type(None)
        else:
            return type(value)

    @staticmethod
    def encode_value(value):
        '''Encode a value using json.dumps, with default = str'''

        return str(value)
