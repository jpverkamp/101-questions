from lib.RedisObject import RedisObject

class QuestionSet(RedisObject):
    def __init__(self, title, questions = []):
        RedisObject.__init__(
            self,
            title = title,
            questions = questions
        )
