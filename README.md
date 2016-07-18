# Interface-Redis

This interface implements the "requires" side of the redis relation.

To use this interface in your layer, you can do something like this:

```python
@when('redis.available')
@when_not('webapp.redis.configured')
def write_redis_configs(redis):
    # Write out redis config params
    status_set('maintenance', 'Configuring Redis cache')

    redis_db = redis_data()[0]

    render('redis.rb',
           target='/srv/webapp/config/redis.rb',
           ctxt=redis_db)

    service_restart('webapp')

    status_set('active', 'Redis cache available'')

    set_state('webapp.redis.configured')
```
