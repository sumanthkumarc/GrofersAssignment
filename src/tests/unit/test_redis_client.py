from api.helpers.redis_client import RedisClient
import os
import pytest


class TestRedisClient:

    @pytest.fixture(scope="module")
    def rc(self):
        db_path = os.environ.get('DB_PATH', "/tmp/redis/data.db")
        return RedisClient(db_path)

    def test_get_key(self, rc):
        rc.set_key("company", "grofers")
        val = rc.get_key("company")
        # Ensure the key returns proper value
        assert val.decode("utf-8") == "grofers"

        val = rc.get_key("company-foo")
        # Ensure the dummy key returns None
        assert not val

    def test_set_key(self, rc):
        rc.set_key("company-bar", "baz")
        val = rc.get_key("company-bar")
        # Ensure the key returns proper value
        assert val.decode("utf-8") == "baz"

    def test_remove_key(self, rc):
        rc.set_key("ping" , "pong")
        val = rc.get_key("ping")
        assert val.decode("utf-8") == "pong"
        rc.remove_key("ping")
        val = rc.get_key("ping")
        assert not val
