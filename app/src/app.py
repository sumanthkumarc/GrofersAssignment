from helpers.redis_client import RedisClient
from flask import Flask, request, Response
import os
import json

port = int(os.environ.get('PORT', 8080))
db_path = os.environ.get('DB_PATH', "/tmp/redis/data.db")
rc = RedisClient(db_path)
app = Flask(__name__)


@app.route('/key/<name>', methods = ['GET', 'DELETE'])
def get_handler(name):
    if request.method == 'GET':
        val = rc.get_key(name)
        if val:
            return {
                "name": name,
                "value": val.decode("utf-8")
            }
        else:
            return Response(status=404)
    elif request.method == 'DELETE':
        rc.remove_key(name)
        return Response(status=204)
    else:
        # Un-allowed method
        return Response(status=405)


@app.route('/key', methods = ['POST'])
def set_handler():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if isinstance(data, str):
            data = json.loads(data)
        # @todo sanitise the value, to remove sql injection etc

        if data.get("name", None) and data.get("value", None):
            rc.set_key(data["name"], data["value"])
            val = rc.get_key(data["name"])
            return {
                "name": data["name"],
                "value": val.decode("utf-8")
            }
        else:
            # Bad request, missing data
            return "Missing one of name or value params", 400
    else:
        # Un-allowed method
        return Response(status=405)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
