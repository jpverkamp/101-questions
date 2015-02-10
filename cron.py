#!/usr/bin/env python3

import sys
if sys.version_info[0] != 3:
    print('Use python3')
    sys.exit()

import datetime

from model.QuestionSet import QuestionSet
import utils

now = datetime.datetime.now()
now = now - datetime.timedelta(minutes = now.minute, seconds = now.second, microseconds = now.microsecond)

for id in QuestionSet.listAllIDs():
    qs = QuestionSet(id)
    if qs.shouldSendNext(now):
        qs.sendNext(now)
