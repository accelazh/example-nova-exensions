import urlparse
from webob import exc

from nova.api.openstack import extensions
from nova.api.openstack import wsgi
from nova.api.openstack import xmlutil
from nova.compute import api
from nova import exception
from pprint import pprint

class Controller(object):
    """Resource extension creates a new resource, which represents a collection of objects.
    Resource controller doesn't need to extend wsgi.Controller
    """

    # the parameter name "exp_res_id" must follow "exp_res" registered in ExtensionDescriptor
    def index(self, req, exp_res_id):
        """Standard REST method: index.
        Mapped to GET: /v2/os-example-resource/{parent_id}/
        """
        return {'data': {
                    'msg': "You are showing child index of parent: %s" % exp_res_id,
                    'parent_id': exp_res_id
               }}

    def show(self, req, exp_res_id, id):
        """Standard REST method: show.
        Mapped to GET: /v2/os-example-resource/{parent_id}/{id}
        """
        return {'data': {
                    'msg': "You are showing child resource object %s of parent %s" % (id, exp_res_id),
                    'parent_id': exp_res_id,
                    'id': id,
                    'parameters': req.GET
               }}

# The name MUST be the same with your .py file, with first letter capitalized.
# Your ExtensionDescriptor must have comment, otherwise won't be loaded.
class Example_child_resource(extensions.ExtensionDescriptor):
    """Example child resource extension creates a new resource. The resource is child of an parent resource object.
    The extension is registered by this class.
    """

    name = "ExampleChildResource"
    # Must follow the naming conversion for extension to work
    alias = "os-example-child-resource"
    namespace = ("http://docs.openstack.org/compute/ext/"
                 "os-example-child-resource/api/v1.2")
    updated = "2014-07-04T00:00:00+08:00"

    def get_resources(self):
        resources = []
        extenion = extensions.ResourceExtension('os-example-child-resource',
                                           controller=Controller(),
                                           parent=dict(                                 # Specify parents here
                                                collection_name="os-example-resource",
                                                member_name="exp_res"))
        resources.append(extenion)
        # You can return a list of resources
        return resources


#########################################
# How to Call
#########################################

# child index
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1/os-example-child-resource' -X GET -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"

# child show
#curl -i 'http://192.168.255.194:8774/v2/16c4a399b6ad4c31b683984bd9188817/os-example-resource/1/os-example-child-resource/2' -X GET -H "X-Auth-Project-Id: admin" -H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: $TOKEN"

