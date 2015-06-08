import flask
import json

from flask.ext.api import status

from lib import RedisObject
from lib.utils import *

def make_blueprint(cls):
    '''Register a class derived from RedisObject with normal REST methods'''

    name = cls.__name__.lower()
    print('registering /api/{0}'.format(name))

    api = flask.Blueprint(name + '_api', __name__, url_prefix = '/api/' + name)

    fields = getattr(cls, 'fields', {})
    lists = getattr(cls, 'lists', {})

    # TODO: automatic permissions

    @api.route('', methods = ['PUT'])
    @renamed('create_' + name)
    def create_obj():
        '''Create a new object, requires all fields to be included as form parameters'''

        params = {
            field : flask.request.form[field]
            for field in fields
        }

        obj = cls(**params)
        return obj.id

    @api.route('/<id>', methods = ['DELETE'])
    @renamed('delete_' + name)
    def delete_obj():
        '''Delete an object by id'''

        obj = cls(flask.request.form['id'])
        obj.delete()

        return json.dumps(True)

    @api.route('/<id>', methods = ['GET'])
    @renamed('read_' + name)
    def read_obj(id):
        '''Read an object by id'''

        obj = cls(id)
        if not obj:
            flask.abort(status.HTTP_404_NOT_FOUND, str(obj) + ' does not exist')

        return repr(obj)

    @api.route('', methods = ['POST'])
    @renamed('update_' + name)
    def update_obj():
        '''Update fields on an object by id; doesn't update list fields'''

        obj = cls(flask.request.form['id'])
        if not obj:
            flask.abort(status.HTTP_404_NOT_FOUND, str(obj) + ' does not exist')

        for field in fields:
            if field in flask.request.form[field]:
                obj['field'] = flask.request.form[field]

        return json.dumps(True)

    for subname in lists:
        # This has to be a function to create a new scope that captures subname
        def bind_subname(subname):
            url_subname = subname.lower()

            @api.route('/<id>/' + url_subname, methods = ['PUT'])
            @renamed('add_' + url_subname + '_to_' + name)
            def add_to_list(id):
                '''
                Add a subobject to this object

                Options:
                - Specify a existing RedisObject's ID to add it to the list
                - Specify all the fields necessary to create a RedisObject to create it and add it
                - Specify 'value' to create other Python primitives
                '''

                obj = cls(id)

                # For RedisObject lists
                if issubclass(lists[subname], RedisObject):
                    # Add already created items by id
                    if 'id' in flask.request.form:
                        subobj = lists[subname](flask.request.form['id'])

                    # Otherwise, create a new object
                    else:
                        params = {
                            field : flask.request.form[field]
                            for field in getattr(lists[subname], 'fields', {})
                        }

                        subobj = lists[subname](**params)

                # For non-RedisObject lists
                else:
                    subobj = lists[subname](flask.request.form['value'])

                if not subobj:
                    flask.abort(status.HTTP_404_NOT_FOUND, str(subobj) + ' does not exist')

                obj.rpush(subname, subobj)

                return json.dumps(True)


            @api.route('/<id>/' + url_subname, methods = ['GET'], defaults = {'lo': 0, 'hi': 10})
            @api.route('/<id>/' + url_subname + '/<int:lo>-<int:hi>', methods = ['GET'])
            @renamed('list_' + url_subname + '_from_' + name)
            def list_from_list(id, lo, hi):

                obj = cls(id)
                subobjs = [lists[subname](subid) for subid in obj.lrange(subname, lo, hi)]

                # TODO: This is ugly, but I think it works?
                return ('[\n' +  ',\n'.join(map(repr, subobjs)) + ']')

            @api.route('/<id>/' + url_subname + '/<int:index>', methods = ['DELETE'])
            @renamed('delete_' + url_subname + '_from_' + name)
            def remove_from_list(id, index):

                obj = cls(id)
                obj.remove(subname, index)

                return json.dumps(True)

            @api.route('/<id>/' + url_subname + '/<int:index>', methods = ['GET'])
            @renamed('read_' + url_subname + '_from_' + name)
            def get_from_list(id, index):

                obj = cls(id)
                return repr(obj.index(subname, index))

            @api.route('/<id>/' + url_subname + '/<int:index>', methods = ['POST'])
            @renamed('update_' + url_subname + '_in_' + name)
            def update_in_list(id):
                '''
                Update a subobject of this object

                Options:
                - For a RedisObject, specify any fields you wish to change
                - For other Python primitives, specify the new 'value'
                '''

                obj = cls(id)

                # For RedisObject lists
                if issubclass(lists[subname], RedisObject):
                    subfields = getattr(lists[subname], 'fields', {})

                    for field in subfields:
                        if field in flask.request.form:
                            obj['subfield'] = subfields[field](flask.request.form[field])

                # For non-RedisObject lists
                else:
                    value = lists[subname](flask.request.form['value'])
                    obj['field'] = value

                return json.dumps(True)

        bind_subname(subname)

    return api
