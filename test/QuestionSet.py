import json

from utils import *

# ----- ----- ----- ----- -----
# Test creating a new quiz
# ----- ----- ----- ----- -----

assert post('/questionset').status_code != 200
assert post('/questionset', data = {
    'title': 'test title'
}).status_code != 200

id = post('/questionset', data = {
    'title': 'test title',
    'frequency': '8 * * *',
    'email': 'test1@example.com'
}).json()['id']

# ----- ----- ----- ----- ----- ----- -----
# Test reading information about that quiz
# ----- ----- ----- ----- ----- ----- -----

assert get('/questionset/{id}', id = id).json()['title'] == 'test title'
assert get('/questionset/{id}/title', id = id).json() == 'test title'
assert get('/questionset/{id}/frequency', id = id).json() == '8 * * *'
assert get('/questionset/{id}/emails', id = id).json() == ['test1@example.com']
assert get('/questionset/{id}/email/0', id = id).json() == 'test1@example.com'

# ----- ----- ----- ----- ----- ----- -----
# Test modified/adding fields to a quiz
# ----- ----- ----- ----- ----- ----- -----

# Title

assert put('/questionset/{id}/title', id = id, data = {'title': 'new test title'}).json()['title'] == 'new test title'
assert get('/questionset/{id}', id = id).json()['title'] == 'new test title'

# Frequency

assert put('/questionset/{id}/frequency', id = id, data = {'frequency': '9 * * *'}).json()['frequency'] == '9 * * *'
assert get('/questionset/{id}', id = id).json()['frequency'] == '9 * * *'

# Emails

response_1 = post('/questionset/{id}/email', id = id, data = {'email': 'test2@example.com'}).json()['emails']
response_2 =  get('/questionset/{id}', id = id).json()['emails']
assert len(response_1) == len(response_2) == 2
assert 'test2@example.com' in response_1 and 'test2@example.com' in response_2

response_1 = post('/questionset/{id}/emails', id = id, data = {'emails': json.dumps(['test3@example.com', 'test4@example.com'])}).json()['emails']
response_2 =  get('/questionset/{id}', id = id).json()['emails']
assert len(response_1) == len(response_2) == 4
assert 'test3@example.com' in response_1 and 'test3@example.com' in response_2

response_1 = put('/questionset/{id}/emails', id = id, data = {'emails': json.dumps(['test5@example.com', 'test6@example.com'])}).json()['emails']
response_2 =  get('/questionset/{id}', id = id).json()['emails']
assert len(response_1) == len(response_2) == 2
assert 'test5@example.com' in response_1 and 'test5@example.com' in response_2

# Questions

post('/questionset/{id}/question', id = id, data = {'question': 'test question 1'}).json()['questions']
response_1 = post('/questionset/{id}/question', id = id, data = {'question': 'test question 2'}).json()['questions']
response_2 =  get('/questionset/{id}', id = id).json()['questions']
assert len(response_1) == len(response_2) == 2
assert 'test question 2' in response_1 and 'test question 2' in response_2

response_1 = post('/questionset/{id}/questions', id = id, data = {'questions': json.dumps(['test question 3', 'test question 4'])}).json()['questions']
response_2 =  get('/questionset/{id}', id = id).json()['questions']
assert len(response_1) == len(response_2) == 4
assert 'test question 3' in response_1 and 'test question 3' in response_2

response_1 = put('/questionset/{id}/questions', id = id, data = {'questions': json.dumps(['test question 5', 'test question 6'])}).json()['questions']
response_2 =  get('/questionset/{id}', id = id).json()['questions']
assert len(response_1) == len(response_2) == 2
assert 'test question 5' in response_1 and 'test question 5' in response_2

# ----- ----- ----- ----- ----- -----
# Test removing fields from a quiz
# ----- ----- ----- ----- ----- -----

response_1 = delete('/questionset/{id}/email/0', id = id).json()['emails']
response_2 =  get('/questionset/{id}', id = id).json()['emails']
assert len(response_1) == len(response_2) == 1
assert 'test5@example.com' not in response_1 and 'test5@example.com' not in response_2

response_1 = delete('/questionset/{id}/question/0', id = id).json()['questions']
response_2 =  get('/questionset/{id}', id = id).json()['questions']
assert len(response_1) == len(response_2) == 1
assert 'test question 4' not in response_1 and 'test question 4' not in response_2

# ----- ----- ----- ----- ----- -----
# Test deleting a quiz
# ----- ----- ----- ----- ----- -----

assert delete('/questionset/{id}', id = id).status_code == 200
assert get('/questionset/{id}', id = id).status_code != 200
