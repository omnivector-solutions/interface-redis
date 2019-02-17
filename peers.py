from charms.reactive import set_flag, clear_flag, when
from charms.reactive import Endpoint


class RedisPeer(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def peer_joined(self):
        set_flag(self.expand_name('peer.joined'))

    @when('endpoint.{endpoint_name}.changed')
    def peer_changed(self):
        set_flag(self.expand_name('peer.changed'))

    @when('endpoint.{endpoint_name}.departed')
    def peer_departed(self):
        set_flag(self.expand_name('peer.departed'))
