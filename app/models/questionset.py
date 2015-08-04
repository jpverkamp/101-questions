import datetime
import lib
import models
import sys

class QuestionSet(lib.RedisDict):
    '''A list of questions that can be combined into a campaign.'''

    def __init__(self, id = None, **defaults):
        '''Create a new questionset: a list of questions sent to one or more users.'''

        lib.RedisDict.__init__(
            self,
            id = id,
            fields = {
                'title': str,
                'frequency': str,
                'targets': lib.RedisList.as_child(self, 'targets', models.User),
                'next-send-date': str,
                'current-question': int,
                'cron-hour': int,
                'questions': lib.RedisList.as_child(self, 'questions', str),
            },
            defaults = defaults
        )

    def shouldSendNext(self):
        '''Check if it's time to send the next question'''

        # If we've already sent all of the questions, we're done
        if self['current-question'] >= len(self['questions']):
            print('Skip: DONE')
            return False

        # The current date is either today or already passed (on misses, send on the next day we catch it)
        now = datetime.datetime.now()
        ymd = now.strftime('%Y-%m-%d')
        if self['next-send-date'] > ymd:
            print('Skip: TOMORROW')
            return False

        # The current hour has to equal the cron hour
        if self['cron-hour'] != now.hour:
            print('Skip: WRONG HOUR')
            return False

        # All conditions pass, send it!
        return True

    def sendNext(self):
        '''Send the next question. Use shouldSendNext to check unless you want to force it.'''

        # TODO: Implement this
        print('Sending question {} from {}'.format(self['current-question'], self))

        # Question sent successfully, increment to the next question
        # TODO: Add more options for this

        self['current-question'] += 1

        now = datetime.datetime.now()
        today = datetime.date(now.year, now.month, now.day)

        frequency = self['frequency'].lower()

        if frequency == 'daily':
            next_day = today + datetime.timedelta(days = 1)
        elif frequency == 'weekly':
            next_day = today + datetime.timedelta(weeks = 1)
        else:
            print('Uknown frequency type "{}", defaulting to daily'.format(frequency))
            next_day = today + datetime.timedelta(days = 1)

        self['next-send-date'] = next_day.strftime('%Y-%m-%d')

        return True
