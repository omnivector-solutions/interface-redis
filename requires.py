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
        Get the connection details.
        """
        redis_data_lst = []
        redis_data_dct = {}
        for conv in self.conversations():
            if conv.get_remote('password'):
                redis_data_dct['password'] = conv.get_remote('password')
            redis_data_dct['port'] = conv.get_remote('port')
            redis_data_dct['private_address'] = \
                conv.get_remote('private-address')
            redis_data_lst.append(redis_data_dct)
        return redis_data_lst
