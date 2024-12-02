class InMemoryCache:
    
    def __init__(self):
        self.cache = {}

    def get(self, key: str):
        return self.cache.get(key, None)

    def set(self, key: str, value: str):
        self.cache[key] = value
