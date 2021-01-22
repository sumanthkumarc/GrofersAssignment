from redislite import Redis
import os
import json


class RedisClient:

    conn = ""
    CHANNEL = "key-update"
    pubsub = ""

    def __init__(self, db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        try:
            if not self.conn:
                self.conn = Redis(db_path)
        except:
            raise Exception("Unable to create connection with Redis server")

    def get_key(self, key):
        return self.conn.get(key)

    def set_key(self, key, value, publish_update=False):
        if publish_update:
            self.publish_update(message=json.dumps({key : value}))

        return self.conn.set(key, value)

    def remove_key(self, key):
        return self.conn.delete(key)

    def publish_update(self, channel=CHANNEL, message=""):
        self.conn.pubsub()
        self.conn.publish(channel, message)

    def get_update(self, channel=CHANNEL):
        if not self.pubsub:
            self.pubsub = self.conn.pubsub()
            self.pubsub.subscribe(channel)

        return self.pubsub.get_message(channel)


