import models
import json
import lib
import flask
import urllib.parse

def register(app):

    @app.route('/friendship/request', methods = ['GET'])
    @lib.authenticated
    def show_friendship_request_page():

        return flask.render_template(
            'import.html',
            redirect = '/user/me',
            action = '/friendship/generate',
            type = 'email address to friend'
        )

    @app.route('/friendship/generate', methods = ['POST'])
    @lib.authenticated
    def generate_friendship_link():

        try:
            target_emails = json.loads(flask.request.form['values'])
        except:
            target_emails = flask.request.form['values'].split('\n')

        if len(target_emails) > 10:
            flask.flash('Cannot send more than 10 invitations at a time')
            return flask.redirect('/friendship/request')

        for target_email in target_emails:
            user = lib.current_user()
            link = user.generateFriendship(target_email)

            url_parts = urllib.parse.urlparse(flask.request.url)
            url = '{scheme}://{host}{link}'.format(
                scheme = url_parts.scheme,
                host = url_parts.hostname,
                link = link
            )

            lib.email(
                emails = [target_email],
                subject = '101 Questions friend request',
                body = '{name} would like to be your friend on 101 Questions.\n\nClick this link to accept: {url}'.format(
                    name = user['name'],
                    url = url,
                )
            )

        flask.flash('{count} invitations sent'.format(count = len(target_emails)))

        if 'redirect' in flask.request.form and flask.request.form['redirect']:
            return flask.redirect(flask.request.form['redirect'])
        else:
            return flask.redirect('/')

    @app.route('/friendship/verify', methods = ['GET'])
    def verify_friendship_link():

        params = {
            key: flask.request.args[key]
            for key in ['src', 'dst', 'sig']
        }

        user = lib.current_user()

        # No user is logged in, send them to the home page
        # Alternatively, the wrong user is logged in, log them out first
        if not user or user['email'] != params['dst']:
            if 'email' in flask.session:
                del flask.session['email']

            flask.flash('Please log in / create an account')
            return flask.render_template('login.html', redirect = flask.request.url)

        # Otherwise, verify and add the friendship
        if user.verifyFriendship(params):
            other = models.User(params['src'])
            flask.flash('Congratulations! You are now friends with {}'.format(other['name']))

        else:
            flask.flash('Could not verify friendship.')

        return flask.redirect('/')
