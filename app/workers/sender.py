import datetime
import lib
import models
import threading
import time

HOURLY_OFFSET = 5

def register(app):

    @lib.daemonize
    def sender_worker():

        while True:
            # Sleep until five minutes past the hour
            now = datetime.datetime.now()
            if now.minute == HOURLY_OFFSET:
                minutes_to_sleep = 60
            else:
                minutes_to_sleep = (60 + HOURLY_OFFSET - now.minute) % 60
            print('sender_worker sleeping for {} minutes'.format(minutes_to_sleep))
            time.sleep(minutes_to_sleep * 60)

            # Scan through all current questionsets
            for user in models.User.all():
                for qs in user['questionsets']:
                    if qs.should_send_next():
                        for i in range(min(1, qs['send-count'])):
                            qs.send_next()
