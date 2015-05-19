from lib.RedisObject import RedisObject

class Answer(RedisObject):
    def __init__(self, text):
        RedisObject.__init__(self, text = text)
