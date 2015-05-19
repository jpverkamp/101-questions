import json
import models
import random
import redis

ID_ALPHABET = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
    'abcdefghijklmnopqrstuvwxyz' +
    '0123456789'
)
ID_LENGTH = 13

class RedisObject(object):
    def __init__(self, id = None, **kwargs):
        self.redis = redis.StrictRedis(host = 'redis')

        if id:
            self.id = id
        else:
            self.id = ''.join(random.choice(ID_ALPHABET) for i in range(ID_LENGTH))

        self.key = self.__class__.__name__ + ':' + self.id
        self.data = {}

        for k, v in kwargs.items():
            self[k] = v

    @classmethod
    def load(cls, id):

        # If the class is in the ID, use that one
        if ':' in id:
            cls_name, id = id.split(':')
            if hasattr(models, cls_name):
                cls = getattr(models, cls_name)

        obj = RedisObject(id)
        obj.__class__ = cls

        obj.id = id
        obj.key = obj.__class__.__name__ + ':' + obj.id

        js = json.loads(
            obj.redis.get(obj.key).decode('utf-8'),
            cls = RedisObjectJSONDecoder
        )
        for k, v in js.items():
            obj.data[k] = v

        return obj

    def save(self):
        self.redis.set(
            self.key,
            json.dumps(
                self.data,
                cls = RedisObjectJSONEncoder
            ).encode('utf-8')
        )

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, val):
        self.data[key] = val

    def __del__(self):
        self.save()

    def __iter__(self):
        for key in self.data:
            yield key

    def __str__(self):
        return self.key + str(self.data)

class RedisObjectJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, RedisObject):
            return {'@ref': o.key}
        else:
            return o

class RedisObjectJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook = self.custom_object_hook, *args, **kwargs)

    def custom_object_hook(self, o):
        if len(o) == 1 and '@ref' in o:
            return RedisObject.load(o['@ref'])
        else:
            return o
