from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class RedisRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:redis}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        if self.redis_data():
            self.set_state('{relation_name}.available')

    @hook('{requires:redis}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')


    def redis_data(self):
        """
        Get the connection details.
        """
        data = {
            'host': self.host(),
            'port': self.port(),
            'database': self.database(),
            'password': self.password(),
        }
        if all(data.values()):
            return data
        return None
