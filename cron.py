#!/usr/bin/env python3

import sys
if sys.version_info[0] != 3:
    print('Use python3')
    sys.exit()

import datetime
import pytz

from model.QuestionSet import QuestionSet
import utils

now = datetime.datetime.now()
now = now - datetime.timedelta(minutes = now.minute, seconds = now.second, microseconds = now.microsecond)

for id in QuestionSet.listAllIDs():
    qs = QuestionSet(id)

    # Verify that the questionset hasn't finished
    if qs['nextQuestion'] >= len(qs['questions']):
        print('qs:{id} is finished'.format(id = qs['id'])) # DEBUG
        continue

    # Verify that we haven't sent a question in the last 12 hours
    if now.timestamp() - qs['lastSent'] < 12 * 60 * 60:
        print('qs:{id} was sent in the last 12 hours'.format(id = qs['id'])) # DEBUG
        continue

    # Check each possible frequency
    fdays, fhour = utils.parseFrequency(qs['frequency'])
    if now.hour != fhour:
        print('qs:{id} does not match current hour (now = {now}, qs = {hour})'.format(id = qs['id'], now = now.hour, hour = fhour)) # DEBUG
        continue

    matchesDate = False
    for fday in fdays:
        if fday[0] == 'monthly' and fday[1] == now.day:
            print('qs:{id} does not match current hour'.format(id = qs['id'])) # DEBUG
            matchesDate = True
        elif fday[0] == 'weekly' and fday[1] == now.weekday:
            print('qs:{id} does not match current hour'.format(id = qs['id'])) # DEBUG
            matchesDate = True
        elif fday[0] == 'daily':
            matchesDate = True

    if not matchesDate:
        print('qs:{id} does not match current date'.format(id = qs['id'])) # DEBUG
        continue

    # Made it this far, send the next question
    emails = qs['emails']
    question = qs['questions'][qs['nextQuestion']]

    print('Send "{question}" to emails'.format(question = question, emails = emails)) # DEBUG

    qs['nextQuestion'] += 1
    qs['lastSent'] = now.timestamp() + 3600
