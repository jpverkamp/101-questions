import base64
import flask
import functools
import json
import os
import random

import controllers

from utils import *
from controllers.flaskrest import make_blueprint

questionset_api = make_blueprint(
    models.QuestionSet,
    lists = {
        'recipients': models.User,
        'questions': str
    }
)

# --- global ---

@questionset_api.route('', methods = ['GET'])
@logged_in
def list_questionsets_for_user():
    '''Get a list of all questionsets for a user'''

    # TODO: Paginate

    return json.dumps(current_user()['questionsets'])
