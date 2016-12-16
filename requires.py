from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class RedisRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:redis}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        conv = self.conversation()
        if conv.get_remote('port'):
            self.set_state('{relation_name}.available')

    @hook('{requires:redis}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    def redis_data(self):
        """
        Return redis connection details.
        """
        conv = self.conversation()
        data = {'host': conv.get_remote('host'),
                'port': conv.get_remote('port'),
                'uri': conv.get_remote('uri')}
        if conv.get_remote('password'):
            data['password'] = conv.get_remote('password')
        return data
