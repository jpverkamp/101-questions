import base64
import json
import redis
import os

class RedisObject(object):
    '''An object backed by redis.'''

    def __init__(self, id = None, **kwargs):
        '''
        Dynamically configure fields:

        fields : {name: cls}
            single objects, cls is the constructor to use
            can use other RedisObjects, they will be serialized by ID

        lists : {name : cls}
            lists of objects to be stored seperately, have to be the same type
            can use RedisObjects
        '''

        self.redis = redis.StrictRedis(host = 'redis', decode_responses = True)
        self.id = id or base64.urlsafe_b64encode(os.urandom(9)).decode('utf-8')

        for k, v in kwargs.items():
            if isinstance(v, list):
                self.rpush(self, k, v)
            else:
                self[k] = v

    def __bool__(self):
        '''
        Test if an object currently exists

        Note: Objects that have not had any of their fields set (this does not include list fields) will return False.
        '''

        name = self.__class__.__name__
        obj_key = '{name}:{id}'.format(name = name, id = self.id)
        return self.redis.exists(obj_key)

    def __eq__(self, other):
        '''Tests if two redis objects are equal (they have the same key)'''

        return isinstance(other, RedisObject) and self.id == other.id

    def delete(self):
        '''Delete an object'''

        name = self.__class__.__name__
        obj_key = '{name}:{id}'.format(name = name, id = self.id)
        self.redis.delete(obj_key)

        lists = getattr(self.__class__, 'lists', {})
        for key in lists:
            obj_key = '{name}:{id}:{key}'.format(name = name, id = self.id, key = key)
            self.redis.delete(obj_key)

    def __getitem__(self, key):
        '''
        Load an attribute from redis.

        id - Return this object's ID directly, doesn't hit redis
        field (key in fields) - Return a field on this object
        list (key in lists) - Return an entire list, use range for just parts
        '''

        name = self.__class__.__name__
        fields = getattr(self.__class__, 'fields', {})
        lists = getattr(self.__class__, 'lists', {})

        if key == 'id':

            return self.id

        elif key in fields:

            obj_key = '{name}:{id}'.format(name = name, id = self.id)

            val = self.redis.hget(obj_key, key)
            return fields[key](val) if val else val

        elif key in lists:

            obj_key = '{name}:{id}:{key}'.format(name = name, id = self.id, key = key)
            vals = self.redis.lrange(obj_key, 0, -1)
            if vals:
                return list(map(lists[key], vals))
            else:
                return []

        print("failed to get {0} in {1}".format(key, self))

    def __setitem__(self, key, val):
        '''
        Set an attribute in redis.

        id - Set this object's ID
        field (key in fields) - Set a object directly, RedisObjects are stored by ID
        list (key in lists) - Doesn't work
        '''

        name = self.__class__.__name__
        fields = getattr(self.__class__, 'fields', {})
        lists = getattr(self.__class__, 'lists', {})

        if key == 'id':

            self.id = val

        elif key in fields:

            obj_key = '{name}:{id}'.format(name = name, id = self.id)
            if isinstance(val, RedisObject):
                val = self.redis.hset(obj_key, key, val.id)
            else:
                val = self.redis.hset(obj_key, key, val)

        elif key in lists:

            raise Exception("Cannot set child lists directly")

    def _redisListWrapper(self, f, key, *args, decode_responses = True):
        '''Helper to do list functions.'''

        name = self.__class__.__name__
        lists = getattr(self.__class__, 'lists', {})

        if not key in lists:
            raise Exception('Not a list: {0}'.format(key))

        obj_key = '{name}:{id}:{key}'.format(name = name, id = self.id, key = key)
        response = f(obj_key, *args)

        if not decode_responses:
            return response
        elif isinstance(response, list):
            return list(map(lists[key], response))
        elif response:
            return lists[key](response)
        else:
            return None

    def lrange(self, key, lo = 0, hi = -1):
        return self._redisListWrapper(self.redis.lrange, key, lo, hi)

    def lpush(self, key, val):
        return self._redisListWrapper(
            self.redis.lpush,
            key,
            val.id if isinstance(val, RedisObject) else val,
            decode_responses = False
        )

    def lpop(self, key):
        return self._redisListWrapper(self.redis.lpop, key)

    def rpush(self, key, val):
        return self._redisListWrapper(
            self.redis.rpush,
            key,
            val.id if isinstance(val, RedisObject) else val,
            decode_responses = False
        )

    def rpop(self, key):
        return self._redisListWrapper(self.redis.rpop, key)

    def length(self, key):
        return self._redisListWrapper(self.redis.llen, key, decode_responses = False)

    def index(self, key, index):
        return self._redisListWrapper(self.redis.lindex, key, index)

    def set(self, key, index, val):
        return self._redisListWrapper(
            self.redis.lset,
            key,
            index,
            val.id if isinstance(val, RedisObject) else val,
            decode_responses = False
        )

    def remove(self, key, index):
        self.set(key, index, '__DELETED__')
        return self._redisListWrapper(self.redis.lrem, key, '__DELETED__', decode_responses = False) == 1

    def __str__(self):
        '''Return this object as a string for testing purposes.'''

        return '{name}:{id}'.format(
            name = self.__class__.__name__,
            id = self.id
        )

    def __repr__(self):
        '''Return a json string representing this RedisObject'''

        fields = getattr(self.__class__, 'fields', {})
        lists = getattr(self.__class__, 'lists', {})

        d = {
            field : self[field]
            for field in fields
        }

        # Only fetch the first ten items for each sublist
        # TODO: Paramaterize the 'ten'?

        if lists:
            d['lists'] = {
                list: {
                    'count': self.length(list),
                    'items': [
                        item.id if issubclass(lists[list], RedisObject) else item
                        for item in self.lrange(list, 0, 10)
                    ]
                } for list in lists
            }

        return json.dumps(d, indent = True, sort_keys = True, default = str)
