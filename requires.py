from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class RedisRequires(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def joined(self):
        if any(unit.received['port'] for unit in self.all_units):
            set_flag(self.expand_name('endpoint.{endpoint_name}.available'))

    @when('endpoint.{endpoint_name}.changed')
    def changed(self):
        if any(unit.received['port'] for unit in self.all_units):
            set_flag(self.expand_name('endpoint.{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('endpoint.{endpoint_name}.available'))

    def relation_data(self):
        """
        Get the list of the relation info for each unit.
        Returns a list of dicts, where each dict contains the host (address)
        and the port (as a string), as well as
        the relation ID and remote unit name that provided the site.
        For example::
            [
                {
                    'host': '10.1.1.1',
                    'port': '80',
                    'relation_id': 'reverseproxy:1',
                    'unit_name': 'myblog/0',
                },
            ]
        """
        services = {}
        for relation in self.relations:
            service_name = relation.application_name
            service = services.setdefault(service_name, {
                'service_name': service_name,
                'hosts': [],
            })
            for unit in relation.units:
                host = unit.received['host']
                port = unit.received['port']
                password = unit.received['password']
                if host and port:
                    ctxt = {'host': host, 'port': port}
                    if password:
                        ctxt['password'] = password

                    service['hosts'].append(ctxt)
        return [s for s in services.values() if s['hosts']]
