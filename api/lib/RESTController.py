import flask
import json

import models

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
            Each element is a pair of (fieldname, subcls)
        '''

        name = cls.__name__.lower()
        print('Binding methods for {0}'.format(name))

        # Read an object
        @app.route('/api/{name}/<id>'.format(name = name), methods = ['GET'])
        @renamed('GET_{name}_BY_ID'.format(name = name))
        def get_object(id):
            obj = cls.load(id)
            data = {key: obj[key] for key in obj if key in visibleFields}
            data['id'] = obj.id

            return json.dumps(data, default = str, indent = True, sort_keys = True)

        # Create a new object
        @app.route('/api/{name}'.format(name = name), methods = ['PUT'])
        @renamed('PUT_{name}'.format(name = name))
        def create_object():
            # Directly casting to dict results in key: [value] rather than key: value
            obj = cls(**{field: flask.request.form[field] for field in flask.request.form})

            return json.dumps(obj.id)

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

        # Mutable list fields can be added to with PUT or removed with DELETE
        if mutableListFields:
            for (mutableListField, subcls) in mutableListFields:
                # Add a previously created item by id
                @app.route('/api/{name}/<id>/{subname}/<subid>'.format(name = name, subname = mutableListField), methods = ['PUT'])
                @renamed('PUT_OLD_{subname}_INTO_{name}'.format(name = name, subname = mutableListField))
                def add_subobject(id, subid):
                    obj = cls.load(id)
                    subobj = subcls.load(subid)
                    obj[mutableListField].append(subobj)

                    return json.dumps(True)

                # Create an add a new subitem directly
                @app.route('/api/{name}/<id>/{subname}'.format(name = name, subname = mutableListField), methods = ['PUT'])
                @renamed('PUT_NEW_{subname}_INTO_{name}'.format(name = name, subname = mutableListField))
                def create_subobject(id):
                    obj = cls.load(id)
                    subobj = subcls(**{field: flask.request.form[field] for field in flask.request.form})
                    obj[mutableListField].append(subobj)

                    return json.dumps(subobj.id)

                # Remove an entry from a mutable list
                @app.route('/api/{name}/<id>/{subname}/<int:index>'.format(name = name, subname = mutableListField), methods = ['DELETE'])
                @renamed('DELETE_{subname}_FROM_{name}'.format(name = name, subname = mutableListField))
                def delete_subobject(id, index):
                    obj = cls.load(id)
                    obj[mutableListField].pop(int(index))

                    return json.dumps(True)
