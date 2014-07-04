import urlparse
from webob import exc

from nova.api.openstack import extensions
from nova.api.openstack import wsgi
from nova.api.openstack import xmlutil
from nova.compute import api
from nova import exception
from pprint import pprint

# Faked db data for the example
DATA = {'1': {'id': '1', 'content': 'It is a ball'},
        '2': {'id': '2', 'content': 'It is a square'},
        '3': {'id': '3', 'content': 'It is a triangle'}}

class Controller(object):
    """Resource extension creates a new resource, which represents a collection of objects.
    Resource controller doesn't need to extend wsgi.Controller
    """

    def index(self, req):
        """Standard REST method: index. 
        Mapped to GET: /v2/os-example-resource
        """
        return {'data': {
                    'msg': "You are showing index",
                    'data': DATA
               }}

    def show(self, req, id):
        """Standard REST method: show.
        Mapped to GET: /v2/os-example-resource/{id}
        """
        return {'data': {
                    'msg': "You are showing resource object: %s" % id,
                    'data': DATA[id],
                    'parameters': req.GET
               }}

    def create(self, req, body=None):
        """Standard REST method: create.
        Mapped to POST: /v2/os-example-resource
        """
        return {'data': {
                    'msg': "You are creating resource object",
                    'parameters': body
               }}

    def update(self, req, id, body=None):
        """Standard REST method: update.
        Mapped to PUT: /v2/os-example-resource/{id}
        """
        return {'data': {
                    'msg': "You are updating resource object: %s" % id,
                    'data': DATA[id],
                    'parameters': body
               }}

    def delete(self, req, id):
        """Standard REST method: delete.
        Mapped to DELETE: /v2/os-example-resource/{id}
        """
        return {'data': {
                    'msg': "You are deleting resource object: %s" % id,
                    'data': DATA[id]
               }}

    # Custom actions need to be decorated. Also need to be registered in ExtensionDescriptor below
    @wsgi.action('custom_action')
    def custom_action(self, req, id):
        """Custom GET action on single resource object.
        Mapped to GET: /v2/os-example-resource/{id}/custom_action
        """
        return {'data': {
                    'msg': "You are doing custom_action on resource object: %s" % id,
                    'data': DATA[id],
                    'parameters': req.GET
               }}

    @wsgi.action('custom_action_update')
    def custom_action_update(self, req, id, body=None):
        """Custom PUT action on single resource object.
        Mapped to PUT: /v2/os-example-resource/{id}/custom_action
        """
        return {'data': {
                    'msg': "You are doing custom_action_update on resource object: %s" % id,
                    'data': DATA[id],
                    'parameters': body
               }}

    @wsgi.action('custom_colleciton_action')
    def custom_collection_action(self, req):
        """Custom GET action collective on all resource objects.
        Mapped to GET: /v2/os-example-resource/custom_collection_action
        """
        return {'data': {
                    'msg': "You are doing custom_colleciton_action on resource objects.",
                    'data': DATA,
                    'parameters': req.GET
               }}

    @wsgi.action('custom_collection_action_update')
    # TODO this method not working right now. Nova-api maps request to self.update(id=custom_collection_action_update)
    def custom_collection_action_update(self, req, body=None):
        """Custom PUT action collective on all resource objects.
        Mapped to PUT: /v2/os-example-resource/custom_collection_action_update
        """
        return {'data': {
                    'msg': "You are doing custom_collection_action_update on resource objects.",
                    'data': DATA,
                    'parameters': body
               }}


# The name MUST be the same with your .py file, with first letter capitalized.
# Your ExtensionDescriptor must have comment, otherwise won't be loaded.
class Example_resource(extensions.ExtensionDescriptor):
    """Example resource extension creates a new resource, which represents a collection of objects.
    The extension is registered by this class.
    """

    name = "ExampleResource"
    # Must follow the naming conversion for extension to work
    alias = "os-example-resource"
    namespace = ("http://docs.openstack.org/compute/ext/"
                 "os-example-resource/api/v1.2")
    updated = "2014-07-04T00:00:00+08:00"

    def get_resources(self):
        resources = []
        extenion = extensions.ResourceExtension('os-example-resource',
                                           controller=Controller(),
                                           member_actions={
                                                'custom_action': "GET",
                                                'custom_action_update': "PUT"},
                                           collection_actions={
                                                'custom_collection_action': "GET",
                                                'custom_collection_action_update': "PUT"})
        resources.append(extenion)
        # You can return a list of resources
        return resources


#########################################
# How to Call
#########################################

# index
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource' -X GET -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"

# show
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1' -X GET -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"

# create
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource' -X POST -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN" -d '{"a":10, "b":13}'

# update
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1' -X PUT -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN" -d '{"a":10, "b":13}'

# delete
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1' -X DELETE -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"

# custom_action
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1/custom_action' -X GET -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"

# custom_action_update
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1/custom_action_update' -X PUT -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN" -d '{"a":10, "b":13}'

# custom_collection_action
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/custom_collection_action' -X GET -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"

# custom_collection_action_update
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/custom_collection_action_update' -X PUT -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN" -d '{"a":10, "b":13}'
