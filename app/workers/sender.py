import datetime
import lib
import models
import sys
import threading
import time

def register(app):

    @lib.daemonize
    def sender_worker():

        while True:
            # Sleep until five minutes past the hour
            now = datetime.datetime.now()
            if now.minute == 5:
                minutes_to_sleep = 60
            else:
                minutes_to_sleep = (65 - now.minute) % 60
            print('sender_worker sleeping for {} minutes'.format(minutes_to_sleep))
            sys.stdout.flush()
            time.sleep(minutes_to_sleep * 60)

            # Scan through all current questionsets
            for user in models.User.all():
                for qs in user['questionsets']:
                    if qs.shouldSendNext():
                        qs.sendNext()
            sys.stdout.flush()
