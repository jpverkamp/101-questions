import flask
import json

from utils import *

BLACKLIST = ['password']

def json_normalize(obj, depth):
    '''Custom function to normalize objects that are 'close enough' to json'''

    # If we've gone too far, just dump it directly
    if depth == 0:
        return obj

    # The object is directly dumpable
    # TODO: This always does it twice, which is sad
    try:
        json.dumps(obj)
        return obj
    except:
        pass

    # Iter over pairs as a dict, dump that
    try:
        return {
            k: json_normalize(v, depth - 1)
            for k, v in obj
            if k not in BLACKLIST
        }
    except:
        pass

    # Iter as keys of a dict, dump that
    try:
        return {
            k: json_normalize(obj[k], depth - 1)
            for k in obj
            if k not in BLACKLIST
        }
    except:
        pass

    # Iter as list items, dump that
    try:
        return [json_normalize(el, depth - 1) for el in obj]
    except:
        pass

    # Last chance, just fall back to default
    return obj

def make_blueprint(cls, lists):
    '''
    Register a dict-like class (that may have list-like subfields) with REST methods

    cls: Constructor, must either be loadable by specifying an ID or creatable with named parameters
    lists: Fields that consist of readable/writeable lists along with constructors for each

    Objects should specify a __bool__ method that returns True/False if they exist.
    Objects should include a delete method that will delete the object and return if it succeeded.
    '''

    name = cls.__name__.lower()
    api = flask.Blueprint(name + '_api', __name__, url_prefix = '/api/' + name)

    print('registering /api/{0}'.format(name))

    # TODO: permissions

    @api.route('/<id>', methods = ['GET'])
    @renamed('read_' + name)
    def read_obj(id):
        '''Read an object by id'''

        obj = cls(id)
        if not obj:
            flask.abort(404, '{} not found: {}'.format(name, id))

        return json.dumps(json_normalize(obj, depth = 3), indent = 2, sort_keys = True, default = str)

    @api.route('', methods = ['PUT'])
    @renamed('create_' + name)
    def create_obj():
        '''Create a new object, requires all fields to be included as form parameters'''

        params = {
            field: flask.request.form[field]
            for field in flask.request.form
        }
        obj = cls(**params)

        return json.dumps(obj.id.rsplit(':', 1)[-1])

    @api.route('/<id>', methods = ['POST'])
    @renamed('update_' + name)
    def update_obj(id):
        '''Update fields on an object by id; doesn't update list fields'''

        obj = cls(id)
        if not obj:
            flask.abort(404, '{} not found: {}'.format(name, id))

        for field in flask.request.form:
            obj[field] = flask.request.form[field]


    @api.route('/<id>', methods = ['DELETE'])
    @renamed('delete_' + name)
    def delete_obj(id):
        '''Delete an object by id. This will fail if the object doesn't have a delete method'''

        obj = cls(id)
        if not obj:
            flask.abort(404, '{} {} not found'.format(name, id))

        result = obj.delete()
        return json.dumps(result)

    for list in lists:
        # This has to be a function to create a new scope that captures list
        def bind_list(list):
            url_list = list.lower()

            @api.route('/<id>/' + url_list + '/<int:index>', methods = ['GET'])
            @renamed('read_' + url_list + '_from_' + name)
            def get_from_list(id, index):
                '''Get a single item from this list'''

                obj = cls(id)
                if not obj:
                    flask.abort(404, '{} not found: {}'.format(name, id))

                subobj = obj[list][index]
                if not subobj:
                    flask.abort(404, '{} not found: {}'.format(list, id))

                return json.dumps(json_normalize(subobj, depth = 3), indent = 2, sort_keys = True, default = str)

            @api.route('/<id>/' + url_list, methods = ['PUT'])
            @renamed('add_' + url_list + '_to_' + name)
            def add_to_list(id):
                '''Add a subobject to this list'''

                obj = cls(id)
                if not obj:
                    flask.abort(404, '{} not found: {}'.format(name, id))

                subcls = lists[list]

                # If we have a value parameter, try that first
                if 'value' in flask.request.form:
                    obj[list].append(subcls(flask.request.form['value']))
                    return json.dumps(True)

                # Otherwise, try to build a subobject
                params = {
                    field: flask.request.form[field]
                    for field in flask.request.form
                }
                subobj = subcls(**params)

                obj[list].append(subobj)

                return json.dumps(subobj.id.rsplit(':', 1)[-1])

            @api.route('/<id>/' + url_list + '/<int:index>', methods = ['POST'])
            @renamed('update_' + url_list + '_in_' + name)
            def update_in_list(id, index):
                '''Update a subobject of this object'''

                obj = cls(id)
                if not obj:
                    flask.abort(404, '{} not found: {}'.format(name, id))

                subcls = lists[list]

                # If we have a value parameter, try that first
                if 'value' in flask.request.form:
                    obj[list][index] = subcls(flask.request.form['value'])
                    return json.dumps(True)

                # Otherwise, get the subobject and update it
                subobj = obj[list][index]
                if not subobj:
                    flask.abort(404, '{} not found: {}'.format(list, id))

                for field in flask.request.form:
                    subobj[field] = flask.request.form[field]

                return json.dumps(True)

            @api.route('/<id>/' + url_list + '/<int:index>', methods = ['DELETE'])
            @renamed('delete_' + url_list + '_from_' + name)
            def remove_from_list(id, index):
                '''Remove an item from this list'''

                obj = cls(id)
                if not obj:
                    flask.abort(404, '{} not found: {}'.format(name, id))

                del obj[list][index]

                return json.dumps(True)

            @api.route('/<id>/' + url_list, methods = ['GET'], defaults = {'lo': 0, 'hi': 10})
            @api.route('/<id>/' + url_list + '/<int:lo>-<int:hi>', methods = ['GET'])
            @renamed('list_' + url_list + '_from_' + name)
            def list_from_list(id, lo, hi):
                '''Get a slice of this list'''

                obj = cls(id)
                if not obj:
                    flask.abort(404, '{} not found: {}'.format(name, id))

                return json.dumps(json_normalize(obj[lo:hi], depth = 2), indent = 2, sort_keys = True, default = str)



        bind_list(list)

    return api
