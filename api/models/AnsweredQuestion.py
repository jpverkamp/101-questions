from models.RedisObject import RedisObject

class AnsweredQuestion(RedisObject):
    def __init__(self, question):
        RedisObject.__init__(
            self,
            question = question,
            answers = []
        )
