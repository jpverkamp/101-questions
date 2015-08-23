
import datetime
import re

def next_weekday(date, match):
    '''Helper function to skip weekends'''

    date += datetime.timedelta(days = 1)
    while date.weekday() >= 5: # Saturday is 5, Sunday is 6
        date += datetime.timedelta(days = 1)

    return date

def next_month(date, match):
    '''Helper function to get the next month, correcting for end of months.'''

    y = date.year
    m = date.month + 1
    d = date.day

    if m == 13:
        y += 1
        m = 1

    while True:
        try:
            return datetime.datetime(y, m, d)
        except:
            d -= 1

def next_list_day(date, match):
    '''Pull apart the list of days.'''

    # Days will be True on the weekday() (see below) that we should match
    valid_days = [False] * 7
    day_names = 'mon tue wed thur fri sat sun'.split()

    for part in match.string.split():
        part = part.lower().strip().strip(',')
        for i, day_name in enumerate(day_names):
            if part.startswith(day_name):
                valid_days[i] = True
                break

    # Advance at least once and then to the next True day
    date += datetime.timedelta(days = 1)
    while not valid_days[date.weekday()]:
        date += datetime.timedelta(days = 1)

    return date

class Frequency(object):

    options = {
        'daily': {
            'regex': 'daily',
            'description': 'once a day',
            'interval': lambda d, m: d + datetime.timedelta(days = 1),
        },
        'weekdays': {
            'regex': 'weekdays?',
            'description': 'same as daily, but skip Saturday and Sunday',
            'interval': next_weekday
        },
        'weekly': {
            'regex': 'weekly',
            'description': 'once per week',
            'interval': lambda d, m: d+ datetime.timedelta(weeks = 1),
        },
        'monthly': {
            'regex': 'monthly',
            'description': 'once per month',
            'interval': next_month,
        },
        'every n days': {
            'regex': 'every (\\d+) days',
            'description': 'every n days, n can be any positive integer',
            'interval': lambda d, m: d + datetime.timedelta(days = int(m.group(1)))
        },
        'list of days': {
            'regex': r'^((mon|tues|wed(?:nes)?|thur(?:s)?|fri|sat(?:ur)?|sun)(?:day)?,?\s*)+$',
            'description': 'a list of days, send only on those days',
            'interval': next_list_day,
        }
    }

    def __init__(self, interval):
        '''Create a new Frequency or throw an exception on invalid specifications.'''

        # Find the internval that matches the given day
        for name in Frequency.options:
            m = re.match(Frequency.options[name]['regex'], interval)

            if m:
                self.interval_string = interval
                self.name = interval
                self.regex = Frequency.options[name]['regex']
                self.description = Frequency.options[name]['description']
                self.interval_function = Frequency.options[name]['interval']
                self.match = m

                return

        raise Exception('Unknown interval: {}'.format(interval))

    @staticmethod
    def options_string():
        '''Return a list of options.'''

        return '\n'.join('- {name}: {description}'.format(
            name = name,
            description = Frequency.options[name]['description'],
        ) for name in Frequency.options)

    def next(self, current):
        '''Given a date, return the next date according to this frequency.'''

        return self.interval_function(current, self.match)

    def __str__(self):

        return self.interval_string
