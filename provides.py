from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class ProvidesRedis(RelationBase):
    scope = scopes.UNIT

    @hook('{provides:redis}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')

    @hook('{provides:redis}-relation-{broken,departed}')
    def broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')
        conv.set_state('{relation_name}.broken')

    def configure(self, port, password=None):
        relation_info = {
            'host': hookenv.unit_get('private-address'),
            'port': port
        }
        if password:
            relation_info['password'] = password
            uri = 'redis://:{password}@{host}:{port}'.format(**relation_info)
        else:
            uri = 'redis://{host}:{port}'.format(**relation_info)
        relation_info['uri'] = uri
        for conv in self.conversations():
            conv.set_remote(**relation_info)
