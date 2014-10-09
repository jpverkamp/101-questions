import datetime
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
def create_user():
    name = randomString(6, mode = 'title') + ' ' + randomString(6, mode = 'title')
    email = name.split()[0].lower() + '@example.com'
    password = randomString(8)

    r = requests.post(API_ROOT + '/user', {'name': name, 'email': email, 'password': password})
    assert r.json(), 'account created successfully'
    user_id = r.json()
    assert re.match('[0-9a-fA-F]{13}', user_id), 'user id is correctly formatted'

    return name, email, password, user_id

name, email, password, user_id = create_user()
other_name, other_email, other_password, other_user_id = create_user()

# Test logins
r = requests.post(ROOT + '/login', {'email': email, 'password': 'invalid'})
assert r.status_code == 400, 'login with invalid password'

r = requests.post(ROOT + '/login', {'email': email})
assert r.status_code == 400, 'login with no password'

session = requests.Session()
r = session.post(ROOT + '/login', {'email': email, 'password': password})
assert r.status_code == 200, 'login with correct password'

other_session = requests.Session()
r = other_session.post(ROOT + '/login', {'email': other_email, 'password': other_password})
assert r.status_code == 200, 'second login with correct password'

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

# Make sure I cannot get other user's information
r = session.get(API_ROOT + '/user/1234567890')
assert r.status_code == 400, "cannot read information about non-existant user"

r = session.get(API_ROOT + '/user/{0}'.format(other_user_id))
assert r.status_code == 400, "cannot read information about unrelated user"

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
qs_id = random.choice(list(qss.keys()))
r = session.get(API_ROOT + '/questionset/{0}'.format(qs_id))
assert qss[qs_id]['title'] == r.json()['title'], 'questionset read back'
assert qss[qs_id]['questions'].split('\n') == r.json()['questions'], 'questionset read back'

r = other_session.get(API_ROOT + '/questionset/1234567890')
assert r.status_code == 400, 'cannot read invalid questionset id'

r = other_session.get(API_ROOT + '/questionset/{0}'.format(qs_id))
assert r.status_code == 400, 'other users cannot read my questionset'

# Test updating a questionset
r = session.put(API_ROOT + '/questionset/{0}'.format(qs_id), {'title': qss[qs_id]['title'] + '(edited)'})
assert 'edited' in r.json()['title'], 'can edit questionset'

r = other_session.put(API_ROOT + '/questionset/{0}'.format(qs_id), {'title': qss[qs_id]['title'] + '(edited)'})
assert r.status_code == 400, 'others cannot edit questions'

r = session.get(API_ROOT + '/questionset/{0}'.format(qs_id))
assert 'edited' in r.json()['title'], 'can read newly edited questionset'

# Test creating a new campaign
today = datetime.datetime.today().date().strftime('%Y-%m-%d')
c_data = {'title': randomTitle(), 'start_date': today, 'frequency': 1}

r = session.post(API_ROOT + '/campaign', c_data)
assert r.status_code == 200, 'create a new campaign'
c_id = r.json()

# Test reading campaigns
r = session.get(API_ROOT + '/campaigns')
assert r.json() == [c_id], 'can read my campaigns'

r = session.get(API_ROOT + '/campaign/{0}'.format(c_id))
assert r.status_code == 200, 'read my own new campaign'
assert r.json()['title'] == c_data['title'], 'verify campaign title was saved'

r = other_session.get(API_ROOT + '/campaign/{0}'.format(c_id))
assert r.status_code == 400, 'others cannot see my campaign'

# Try changing basic fields on a campaign
r = session.put(API_ROOT + '/campaign/{0}'.format(c_id), {'title': c_data['title'] + ' (edited)'})
assert r.status_code == 200, 'edit my own campaign'
assert 'edited' in r.json()['title'], 'verify campaign title was edited'

r = session.get(API_ROOT + '/campaign/{0}'.format(c_id))
assert 'edited' in r.json()['title'], 'verify campaign title was edited on read'

r = other_session.put(API_ROOT + '/campaign/{0}'.format(c_id), {'title': c_data['title'] + ' (edited)'})
assert r.status_code == 400, 'others cannot edit my campaign'

# Try changing campaign questions
new_qs = []
for qs_id, qs in qss.items():
    for i in range(len(qs['questions'].split('\n'))):
        new_qs.append([qs_id, i])
random.shuffle(new_qs)
new_qs_str = '\n'.join(['{0}.{1}'.format(*each) for each in new_qs])

r = session.put(API_ROOT + '/campaign/{0}'.format(c_id), {'questions': new_qs_str})
assert r.status_code == 200, 'can edit questions'

r = session.get(API_ROOT + '/campaign/{0}'.format(c_id))
assert r.json()['questions'] == new_qs, 'questions saved correctly to campaign'

r = session.put(API_ROOT + '/campaign/{0}'.format(c_id), {'questions': '1234567890.0'})
assert r.status_code == 400, 'cannot add questions from invalid questionset'

r = session.put(API_ROOT + '/campaign/{0}'.format(c_id), {'questions': 'error.error'})
assert r.status_code == 400, 'cannot add inproperly formatted questions'

print('All tests passed successfully!')
