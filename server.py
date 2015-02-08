import flask

app = flask.Flask('101qs')
app.debug = True

import controller.QuestionSet
controller.QuestionSet.init(app)

@app.route('/', methods = ['get'])
def root():
    return app.send_static_file('index.htm')

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 10177
    )
