from models.RedisObject import RedisObject

class QuestionRun(RedisObject):
    def __init__(self, title, start_date, frequency, users = None, questionsets = None, questions = None):

        users = users or []
        questions = questions or []

        if questionsets:
            for questionset in questionsets:
                for question in questionset['questions']:
                    questions.append(question)

        RedisObject.__init__(
            self,
            title = title,
            start_date = start_date,
            frequency = frequency,
            users = users,
            questions = questions
        )
