import flask
import json

def renamed(new_name):
    def inner(f):
        f.__name__ = new_name
        return f
    return inner

class RESTController(object):

    def __init__(
        self,
        app,
        cls,
        visibleFields = None,
        mutableFields = None,
        mutableListFields = None,
    ):
        '''
        Bind default REST endpoints for an object.

        :param app: The Flask application to add routes to
        :param cls: The class that will be wrapped
        :param visibleFields: fields that will appear in GET /object/id
        :param mutableFields: fields that can be changed with POST /object/id, must be visible
        :param mutableListFields: fields with child objects that you can PUT or DELETE to, /object/id/subobject/id
        '''

        name = cls.__name__.lower()
        print('Binding methods for {0}'.format(name))

        # Read an object
        @app.route('/api/{name}/<id>'.format(name = name), methods = ['GET'])
        @renamed('GET_{name}_BY_ID'.format(name = name))
        def get_object(id):
            obj = cls.load(id)
            data = {key: obj[key] for key in obj if key in visibleFields}
            return json.dumps(data, indent = True, sort_keys = True)

        # Create a new object
        @app.route('/api/{name}'.format(name = name), methods = ['PUT'])
        @renamed('PUT_{name}'.format(name = name))
        def create_object():

            import sys
            sys.stdout.flush()

            # Directly casting to dict results in key: [value] rather than key: value
            obj = cls(**{field: flask.request.form[field] for field in flask.request.form})

            return json.dumps(True)
            #return get_object(obj.id)

        # Modify one or more fields on an object
        @app.route('/api/{name}/<id>'.format(name = name), methods = ['POST'])
        @renamed('POST_{name}_BY_ID'.format(name = name))
        def update_fields(id):
            for field in flask.request.form:
                if not field in mutableFields:
                    flask.abort(403) # Forbidden

            obj = cls.load(id)

            for field in flask.request.form:
                value = flask.request.form[field]
                obj[field] = value

            obj.save()

            return json.dumps(True)
            #return get_object(obj.id)
