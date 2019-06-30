from charms.reactive import Endpoint


class RedisProvides(Endpoint):

    def configure(self, host, port, password=None):
        """
        Configure the host-port relation by providing a port and host.
        """
        ctxt = {'host': host, 'port': port}
        if password:
            ctxt['password'] = password
        for relation in self.relations:
            relation.to_publish.update(ctxt)
