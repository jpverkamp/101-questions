import models
import flask

def register(app):

    @app.route('/', methods = ['GET'])
    def home():
        if 'email' in flask.session:
            current_user = models.User(flask.session['email'])
            return flask.render_template('user.html', user = current_user)
        else:
            return flask.render_template('login.html')

    @app.route('/login', methods = ['POST'])
    def login():
        email = flask.request.form['email']
        password = flask.request.form['email']

        u = models.User(email)
        if u and u.verifyPassword(password):
            flask.session['email'] = email
        else:
            flask.flash('Incorrect username or password')

        if 'redirect' in flask.request.form and flask.request.form['redirect']:
            return flask.redirect(flask.request.form['redirect'])
        else:
            return flask.redirect('/')

    @app.route('/logout', methods = ['GET', 'POST'])
    def logout():

        if 'email' in flask.session:
            del flask.session['email']

        flask.flash('Logged out')

        return flask.redirect('/')

    @app.route('/register', methods = ['POST'])
    def register():
        name = flask.request.form['name']
        email = flask.request.form['email']
        password = flask.request.form['email']

        u = models.User(name = name, email = email, password = password)
        flask.session['email'] = email

        flask.flash('New user created')

        if 'redirect' in flask.request.form and flask.request.form['redirect']:
            return flask.redirect(flask.request.form['redirect'])
        else:
            return flask.redirect('/')
