import redis


class RedisSemanticCache:
    
    def __init__(self, redis_url: str, embedding=None):
        self.redis_client = redis.StrictRedis.from_url(redis_url)
        self.embedding = embedding

    def get(self, key: str):
        cached_value = self.redis_client.get(key)
        if cached_value:
            return cached_value.decode('utf-8')
        return None

    def set(self, key: str, value: str):
        self.redis_client.set(key, value)
