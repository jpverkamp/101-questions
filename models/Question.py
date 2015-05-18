from models.RedisObject import RedisObject

class Question(RedisObject):
    def __init__(self, text):
        RedisObject.__init__(self, text = text)
