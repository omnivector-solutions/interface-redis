from charms.reactive import when
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class RedisProvides(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def joined(self):
        set_flag('endpoint.{endpoint_name}.available')

    @when('endpoint.{endpoint_name}.broken')
    def broken(self):
        set_flag('endpoint.{endpoint_name}.broken')

    def configure(self, host, port, password=None):
        """
        Configure the host-port relation by providing a port and host.
        """
        ctxt = {'host': host, 'port': port}
        if password:
            ctxt['password'] = password
 
        for relation in self.relations:
            relation.to_publish_raw.update(ctxt)
