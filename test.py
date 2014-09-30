
def init(app):

    app.checkPermissions = False

    import model.user

    test_user = model.user.byEmail(app, 'me@jverkamp.com')
    if not test_user:
        test_user = model.user.User(
            app,
            name = 'JP Verkamp',
            email = 'me@jverkamp.com',
        )

    test_user.setPassword('password')
    print('test user: {0}'.format(test_user.id))

    import model.questionset

    if False:
        test_qs = model.questionset.QuestionSet(
            app,
            title = 'Hello',
            questions = [
                'World?',
                'Kitty?',
                'Goodbye?',
            ]
        )

        print('test questionset: {0}'.format(test_qs.id))
        test_user.setPermission(test_qs, 'read')

    print('-----')

    print('all things')
    print(list(test_user.getResources()))

    print('all questionsets')
    print(list(test_user.getResources('QuestionSet')))

    print('all things with <= write permission')
    print(list(test_user.getResources(permission = 'write')))

    print('all questionsets, ids only')
    print(list(test_user.getResources('QuestionSet', id_only = True)))

    app.checkPermissions = True

if __name__ == '__main__':

    import requests
    s = requests.Session()

    ROOT = 'http://localhost:5000/api/v1'

    r = s.post(ROOT + '/user/login', {
        'email': 'me@jverkamp.com',
        'password': 'password'
    })
    print(dict(r.cookies))

    print(s.get(ROOT + '/user/me').text)
    print(s.get(ROOT + '/user/619f47f32a036').text)

    qs_ids = s.get(ROOT + '/questionsets')
    print(qs_ids.text)
    for qs_id in qs_ids.json():
        print(s.get(ROOT + '/questionset/' + qs_id).text)
