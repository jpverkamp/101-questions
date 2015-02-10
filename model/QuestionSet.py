import datetime

import model.Mailer
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

    def shouldSendNext(self, now):
        '''
        Return True if the next question should be sent this hour.

        now should specify the hour in which to send the object
        '''

        if not now:
            now = datetime.datetime.now()
            now = now - datetime.timedelta(minutes = now.minute, seconds = now.second, microseconds = now.microsecond)

        # Verify that the questionset hasn't finished
        if self['nextQuestion'] >= len(self['questions']):
            print('NOSEND qs:{id} is finished'.format(id = self['id'])) # DEBUG
            return False

        # Verify that we haven't sent a question in the last 12 hours
        if now.timestamp() - self['lastSent'] < 12 * 60 * 60:
            print('NOSEND qs:{id} was sent in the last 12 hours'.format(id = self['id'])) # DEBUG
            return False

        # Check each possible frequency
        fdays, fhour = utils.parseFrequency(self['frequency'])
        if now.hour != fhour:
            print('NOSEND qs:{id} does not match current hour (now = {now}, self = {hour})'.format(id = self['id'], now = now.hour, hour = fhour)) # DEBUG
            return False

        matchesDate = False
        for fday in fdays:
            if fday[0] == 'monthly' and fday[1] == now.day:
                print('?SEND? qs:{id} does not match current hour'.format(id = self['id'])) # DEBUG
                matchesDate = True
            elif fday[0] == 'weekly' and fday[1] == now.weekday:
                print('?SEND? qs:{id} does not match current hour'.format(id = self['id'])) # DEBUG
                matchesDate = True
            elif fday[0] == 'daily':
                matchesDate = True

        if not matchesDate:
            print('NOSEND qs:{id} does not match current date'.format(id = self['id'])) # DEBUG
            return False

        # If we made it this far, we have a match!
        return True

    def sendNext(self, now = None):
        '''
        Send the next question (use shouldSendNext to check if required).

        now should specify the hour in which to send the object
        '''

        if not now:
            now = datetime.datetime.now()
            now = now - datetime.timedelta(minutes = now.minute, seconds = now.second, microseconds = now.microsecond)

        # Made it this far, send the next question
        emails = self['emails']
        subject = '{title}: Day {index} of {count}'.format(
            title = self['title'],
            index = self['nextQuestion'] + 1,
            count = len(self['questions'])
        )
        body = self['questions'][self['nextQuestion']]

        model.Mailer.send(emails = emails, subject = subject, body = body)

        self['nextQuestion'] += 1
        self['lastSent'] = now.timestamp() + 3600
