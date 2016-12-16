from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class ProvidesRedis(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:redis}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')

    @hook('{provides:redis}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.connected')

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

        self.set_remote(**relation_info)
        self.set_state('{relation_name}.configured')
