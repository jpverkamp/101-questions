from model.Model import Model

class QuestionSet(Model):

    def __init__(self, id, **data):
        '''
        Create a new questionset

        title is just a string
        frequency is a subset of cron format without the minute field
        email is a valid email address, more can be added later
        '''

        Model.__init__(self, id, **data)
