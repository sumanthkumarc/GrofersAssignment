import os
from api.helpers.redis_client import RedisClient
from flask import Flask


db_path = os.environ.get('DB_PATH', "/tmp/redis/data.db")
rc = RedisClient(db_path)
app = Flask(__name__)