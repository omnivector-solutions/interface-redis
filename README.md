# Interface-Redis

### Implementation
Layers leveraging this interface can react to the `'endpoint.redis.available'` flag
set on the requires side of the interface/relationship.


### Example
When a relationship is created via the redis interface, the flag `'endpoint.redis.available'` will be
set active in the relating charm.

```bash
juju deploy cs:~omnivector/redis

juju deploy my-test-charm

juju relate my-test-charm redis
```

Where `my-test-charm` could resemble the following

```yaml
# layer.yaml
includes: 
  - 'layer:basic'
  - 'interface:redis'
```
```yaml
# metadata.yaml

name:  my-test-charm
summary: my-test-charm
maintainer: James Beedy <jamesbeedy@gmail.com>
description: |
  test-charm
tags:
  - test
series:
  - bionic
requires:
  redis:
    interface: redis
```

```python
# my_test_charm.py

from charms.reactive import (
    when,
    when_not,
    set_flag,
    endpoint_from_flag,
)

from charmhelpers.core.hookenv import status_set
from charmhelpers.core import unitdata


KV = unitdata.kv()


@when('endpoint.redis.available')
@when_not('my-test-charm.redis.available')
def get_set_redis_connection_info():
    """ Save redis connection info to unitdata.
    """
    status_set('maintenance', 'Getting redis connection info')

    endpoint = endpoint_from_flag('endpoint.redis.available')

    KV.set('redis_host', endpoint.relation_data()[0]['host'])
    KV.set('redis_port', endpoint.relation_data()[0]['port'])

    status_set('active', 'Redis connection info received')
    set_flag('my-test-charm.redis.available')
```


#### Copyright
* James Beedy (c) 2018 <jamesbeedy@gmail.com>

#### License
* AGPLv3 (see `LICENSE` file)

