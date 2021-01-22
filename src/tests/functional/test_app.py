import pytest
from run import app
import json


@pytest.fixture(scope="module")
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_get_key(client):
    body = {
        "name" : "gryffindor",
        "value": "harry"
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = client.post("/key",json=json.dumps(body), headers=headers)
    assert r.status_code == 200

    r = client.get("/key/gryffindor")
    assert r.status_code == 200
    data = r.json
    assert data["name"] == "gryffindor"
    assert data["value"] == "harry"

    # Obviously it's not house in Hogwarts, it's a school.
    r = client.get("/key/durmstrang")
    assert r.status_code == 404

    # Can't update house data like this. Use set method.
    r = client.post("/key/gryffindor", json="")
    assert r.status_code == 405


def test_set_key(client):
    body = {
        "name" : "gryffindor",
        "value": "hermione"
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = client.post("/key",json=json.dumps(body), headers=headers)
    assert r.status_code == 200

    r = client.get("/key/gryffindor")
    assert r.status_code == 200
    data = r.json
    assert data["name"] == "gryffindor"
    assert data["value"] == "hermione"

    body = {
        "name": "gryffindor",
        "value": "ron"
    }

    r = client.post("/key", json=json.dumps(body), headers=headers)
    assert r.status_code == 200

    r = client.get("/key/gryffindor")
    assert r.status_code == 200
    data = r.json
    assert data["name"] == "gryffindor"
    assert data["value"] == "ron"


def test_delete_key(client):
    body = {
        "name": "slytherin",
        "value": "draco"
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = client.post("/key", json=json.dumps(body), headers=headers)
    assert r.status_code == 200
    data = r.json
    assert data["name"] == "slytherin"
    assert data["value"] == "draco"

    r = client.delete("/key/slytherin")
    assert r.status_code == 204

    r = client.get("/key/slytherin")
    assert r.status_code == 404
