import redis
from setting.database_setting import REDIS_HOST, REDIS_PORT


class Redis(object):
    def __init__(self, pool_size=5):
        self.conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def hget(self, name, key):
        return self.conn.hget(name, key)

    def hset(self, name, key, value):
        return self.conn.hset(name, key, value)

    def hdel(self, name, key):
        return self.conn.hdel(name, key)

    def hkeys(self, name):
        return self.conn.hkeys(name)

    def __del__(self):
        self.conn.close()


redis_conn = Redis()

if __name__ == "__main__":
    print(redis_conn.hset("try", "t1", "1"))
    r = redis_conn.hget("try", "t1")
    r = r.decode()
    print(r, type(r))
    r = redis_conn.hdel("try", "t1")
    print(r, type(r))
    r = redis_conn.hkeys("count_cache")
    for k in r:
        k = k.decode()
        print(k)
        redis_conn.hdel("count_cache", k)
