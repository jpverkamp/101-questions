import flask
import os

from flask.ext.api import status

ui_api = flask.Blueprint('ui_api', __name__)

templates = {}

with open(os.path.join('templates', '_base.html'), 'r') as fin:
    base_template = fin.read()

for template in os.listdir('templates'):
    if not template.endswith('.html'):
        continue

    if template.startswith('_'):
        continue

    with open(os.path.join('templates', template), 'r') as fin:
        template_name = template.rsplit('.', 1)[0]
        template_content = fin.read()
        templates[template_name] = base_template.format(content = template_content)

@ui_api.route('/<controller>/<id>', methods = ['GET'])
def render(controller, id):

    if not controller in templates:
        flask.abort(status.HTTP_404_NOT_FOUND, 'Template not found for {controller}'.format(controller = controller))

    return templates[controller]

@ui_api.route('/', methods = ['GET'])
def home():
    return templates['login']
