import urlparse
from webob import exc
from pprint import pprint

from nova.api.openstack import extensions
from nova.api.openstack import wsgi
from nova.api.openstack import xmlutil
from nova.compute import api
from nova import exception

# extension controller must extend wsgi.Controller
class Controller(wsgi.Controller):
    """Controller extension extends a existing resource. 
    Must extend wsgi.Controller.
    """

    # Must decorated by @wsgi.extends to extend original show() method
    @wsgi.extends
    def show(self, req, resp_obj, id):
        """Extend the original show() method
        """
        resp_obj.obj['data']['extends']={
            'msg': "This is extended show()",
            'id': id,
            'parameters': req.GET
        }

    @wsgi.extends
    def custom_action_update(self, req, resp_obj, id, body=None):
        """Extend the original PUT custom_action_update() method
        """
        resp_obj.obj['data']['extends']={
            'msg': "This is extended custom_action_update()",
            'id': id,
            'parameters': body
        }

    # TODO this one isn't working. Maybe nova-api doesn't support it.
    @wsgi.action('custom_extend')
    def custom_extend(self, req, id):
        """Add a new custom action
        Mapped to GET /v2/os-example-resource/{id}/custom_extend
        """
        return {'data': {
                    'msg': "This custom_extend() on resource object: %s" % id,
                    'id': id,
                    'parameters': req.GET
               }}


# The name MUST be the same with your .py file, with first letter capitalized.
# Your ExtensionDescriptor must have comment, otherwise won't be loaded.
class Example_controller_extension(extensions.ExtensionDescriptor):
    """Controller extension extends existing resources.
    The extension is registered by this class
    """

    name = "ExampleControllerExtension"
    # Must follow the naming conversion for extension to work
    alias = "os-example-controller-extension"
    namespace = ("http://docs.openstack.org/compute/ext/"
                 "os-example-controller-extension/api/v1.2")
    updated = "2014-07-04T00:00:00+08:00"

    def get_controller_extensions(self):
        controller = Controller()
        extension = extensions.ControllerExtension(self, 'os-example-resource', controller)
        # You can return a list of resources
        return [extension]


#######################################
# How to call
#######################################

# show
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1' -X GET -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"

# custom_action_update
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1/custom_action_update' -X PUT -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN" -d '{"a":10, "b":13}'

# custom_extend
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1/custom_extend' -X GET -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"

