import time

import redis


with redis.Redis() as client:
    client.set('foo', 'bar')
    client.get('foo')
