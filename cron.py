#!/usr/bin/env python3

import sys
if sys.version_info[0] != 3:
    print('Use python3')
    sys.exit()

import datetime
import parsedatetime

from model.QuestionSet import QuestionSet

now = datetime.datetime.now()
now = now - datetime.timedelta(minutes = now.minute, seconds = now.second, microseconds = now.microsecond)

parse = parsedatetime.Calendar().parse

for id in QuestionSet.listAllIDs():
    qs = QuestionSet(id)

    # Verify that the questionset hasn't finished
    if qs['nextQuestion'] >= len(qs['questions']):
        print('qs:{id} is finished'.format(id = qs['id'])) # DEBUG
        continue

    # Calculate when the next message should be sent
    nextRun, _ = parse(
        qs['frequency'],
        qs['lastSent'] and datetime.datetime.fromtimestamp(qs['lastSent'])
    )
    nextRun = datetime.datetime(*nextRun[:4])

    print('Comparing now:{now} and next:{nextRun}'.format(now = now, nextRun = nextRun)) # DEBUG

    # Send the next message (either it's up now or we missed an interval)
    if nextRun <= now:

        emails = qs['emails']
        question = qs['questions'][qs['nextQuestion']]

        print('Send "{question}" to emails'.format(question = question, emails = emails)) # DEBUG

        qs['nextQuestion'] += 1
        qs['lastSent'] = now.timestamp() + 3600
