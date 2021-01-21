from redislite import Redis
import os


class RedisClient:

    conn = ""

    def __init__(self, db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        try:
            if not self.conn:
                self.conn = Redis(db_path)
        except:
            raise Exception("Unable to create connection with Redis server")

    def get_key(self, key):
        return self.conn.get(key)

    def set_key(self, key, value):
        return self.conn.set(key, value)

    def remove_key(self, key):
        return self.conn.delete(key)