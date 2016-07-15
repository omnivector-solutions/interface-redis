# Interface-Redis

This interface implements the "requires" side of the redis relation.

To use this interface in your layer, you can do something like this:

```python
@when('redis.available')
@when_not('redis.configured')
def write_redis_configs(redis):
    # Write out redis config params

    status_set('maintenance', 'Configureing Redis cache')

    render('redis.conf, redis)

    service_restart('webapp')

    status_set('active', 'Redis cache available'')

    set_state('redis.configured')
```
