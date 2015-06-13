import base64
import flask
import functools
import json
import os
import random

from flask.ext.api import status

import models

from lib.utils import *
from lib import make_blueprint

questionset_api = make_blueprint(models.QuestionSet)

# --- global ---

@questionset_api.route('', methods = ['GET'])
@logged_in
def list_questionsets_for_user():
    '''Get a list of all questionsets for a user'''

    # TODO: Paginate

    return json.dumps(current_user()['questionsets'])
