import os
import requests

def email(emails, subject, body):
    response = requests.post(
        'https://api.mailgun.net/v3/mail.101qs.jverkamp.com/messages',
        auth = ('api', os.environ['MAILGUN_API_KEY']),
        data = {
            'from': '101 Questions <mailgun@mail.101qs.jverkamp.com>',
            'to': ', '.join(emails),
            'subject': subject,
            'text': body,
            'h:Reply-To': ', '.join(emails)
        })

    if response:
        print('Sent {} to {}'.format(
            subject,
            emails,
        ))
    else:
        print('Failed to send {} to {}: {}'.format(
            subject,
            emails,
            response.text,
        ))

