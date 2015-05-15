import copy
import smtplib
import os

EMAIL_TEMPLATE = '''From: 101-questions@jverkamp.com
Reply-To: {src}
To: {dst}
Subject: {subject}
Content-Type: text/plain; charset=utf-8; format=flowed

{body}'''

class Mailer(object):
    instance = None

    def __init__(self):
        host = os.environ['EMAIL_HOST']
        port = int(os.environ['EMAIL_PORT'])

        self.smtp = smtplib.SMTP_SSL(host, port)
        self.smtp.ehlo()
        self.smtp.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])

    def __del__(self):
        self.smtp.close()

def send(emails, subject, body, second_chance = False):

    if Mailer.instance == None:
        Mailer.instance = Mailer()

    try:

        for dst in emails:
            if len(emails) == 1:
                src = '101-questions@jverkamp.com'
            else:
                srcList = copy.copy(emails)
                srcList.remove(dst)
                src = '; '.join(srcList)


            if src == dst:
                continue

            msg = EMAIL_TEMPLATE.format(
                src = src,
                dst = dst,
                subject = subject,
                body = body
            )
            print('Mailing {subject} to {dst}'.format(subject = subject, dst = dst))

            Mailer.instance.smtp.sendmail(os.environ['EMAIL_USER'], dst, msg)

    except Exception as ex:

        print('Failure in mailer: {0}'.format(ex))

        if not second_chance:
            # Most likely failure is that the SMTP connection timed out
            # Try to rebuild it and resend, only try one extra time though
            Mailer.instance = Mailer()
            send(emails, subject, body, True)