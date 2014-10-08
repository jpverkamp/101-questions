import random
import re
import requests

ROOT = 'http://localhost:5000'
API_ROOT = 'http://localhost:5000/api/v1'

def randomString(length = None, mode = 'upper'):
    if not length:
        length = random.randint(1, 16)

    new_str = ''.join([
        random.choice('BCDFGHJKLMNPQRSTVWXYZ' if i % 2 == 0 else 'AEIOU')
        for i in range(length)
    ])

    if mode == 'upper':
        return new_str
    elif mode == 'lower':
        return new_str.lower()
    elif mode == 'title':
        return new_str[0].upper() + new_str[1:].lower()

# Create a new account
name = randomString(6, mode = 'title') + ' ' + randomString(6, mode = 'title')
email = name.split()[0].lower() + '@example.com'
password = randomString(8)

r = requests.post(API_ROOT + '/user', {'name': name, 'email': email, 'password': password})
assert r.json(), 'account created successfully'
user_id = r.json()
assert re.match('[0-9a-fA-F]{13}', user_id), 'user id is correctly formatted'

# Test logins
r = requests.post(ROOT + '/login', {'email': email, 'password': 'invalid'})
assert r.status_code == 400, 'login with invalid password'

r = requests.post(ROOT + '/login', {'email': email})
assert r.status_code == 400, 'login with no password'

session = requests.Session()
r = session.post(ROOT + '/login', {'email': email, 'password': password})
assert r.status_code == 200, 'login with correct password'

# Try to get my own user information
# Have to be logged in for this, ergo the use of session
r = session.get(API_ROOT + '/user/me')
assert r.json()['name'] == name, '/user/me correctly stored name'
assert r.json()['email'] == email, '/user/me correctly stored email'
assert not 'password' in r.json(), '/user/medid not return password'

# Try to get my information by user id
r = session.get(API_ROOT + '/user/{0}'.format(user_id))
assert r.json()['name'] == name, '/user/<id> correctly stored name'
assert r.json()['email'] == email, '/user/<id> correctly stored email'
assert not 'password' in r.json(), '/user/<id> did not return password'

# Test creating questionsets
def randomTitle():
    return randomString(mode = 'title') + randomString(mode = 'lower')

def randomQuestion():
    q = randomString(mode = 'title')
    for i in range(random.randint(1, 6)):
        q += ' ' + randomString(mode = 'lower')
    q += '?'
    return q

def randomQuestions(count):
    return [randomQuestion() for i in range(count)]

r = requests.post(API_ROOT + '/questionset', {
    'title': randomTitle(),
    'questions': '\n'.join(randomQuestions(10))
})
assert r.status_code == 400, 'questionset without signing in'

qss = {}
for i in range(3):
    qs = {
        'title': randomTitle(),
        'questions': '\n'.join(randomQuestions(10))
    }
    r = session.post(API_ROOT + '/questionset', qs)
    assert r.status_code == 200, 'questionset created'
    qss[r.json()] = qs

# Test reading all question sets for a user
r = session.get(API_ROOT + '/questionsets')
assert set(qss.keys()) == set(r.json()), 'questionsets are readable'

# Test reading a specific questionset
qs_id = random.choice(qss.keys())
r = session.get(API_ROOT + '/questionset/{0}'.format(qs_id))
assert qss[qs_id]['title'] == r.json()['title'], 'questionset read back'
assert qss[qs_id]['questions'].split('\n') == r.json()['questions'], 'questionset read back'


print('All tests passed successfully!')
