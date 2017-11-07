from charms.reactive import when_any, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class RedisRequires(Endpoint):
    @when_any('endpoint.{relation_name}.changed.host',
              'endpoint.{relation_name}.changed.port',
              'endpoint.{relation_name}.changed.password')
    def relation_state_modified(self):
        # Detect changes to the host or port field on any remote unit
        # and translate that into the host-port flag. Then, clear the
        # changed field flags so that we can detect further changes.
        set_flag(self.flag('endpoint.{relation_name}.host-port'))
        clear_flag(self.flag('endpoint.{relation_name}.changed.host'))
        clear_flag(self.flag('endpoint.{relation_name}.changed.port'))
        clear_flag(self.flag('endpoint.{relation_name}.changed.password'))

    @when_not('endpoint.{relation_name}.joined')
    def broken(self):
        clear_flag(self.flag('endpoint.{relation_name}.host-port'))

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
        units_data = []
        for relation in self.relations:
            for unit in relation.units:
                host = unit.received['host']
                port = unit.received['port']
                password = unit.received['password']
                if not (host and port):
                    continue
                ctxt = {}
                if password:
                    ctxt['password'] = password
                ctxt['host'] = host
                ctxt['port'] = port
                ctxt['relation_id'] = relation.relation_id
                ctxt['unit_name'] = unit.unit_name
                units_data.append(ctxt)
        return units_data

