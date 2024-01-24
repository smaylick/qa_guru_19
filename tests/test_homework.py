import json
from jsonschema import validate

import requests

base_url = "https://reqres.in/api/"


def test_get_user():
    response = requests.get(f"{base_url}users/2")
    assert response.json()["data"]["first_name"] == "Janet"


def test_create_user():
    name = "Anton"
    job = "QA"
    response = requests.post(f"{base_url}users", json={
        "name": name,
        "job": job
    })
    assert response.status_code == 201
    assert response.json()["name"] == name
    assert response.json()["job"] == job


def test_update_user():
    name = "Sergey"
    job = "Teacher"
    response = requests.put(f"{base_url}users/2", json={
        "name": name,
        "job": job
    })
    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["job"] == job


def test_delete_user():
    response = requests.delete(f"{base_url}users/2")
    assert response.status_code == 204


def test_get_list_users():
    response = requests.get(f"{base_url}users", params={
        "page": 2
    })
    body = response.json()
    with open("files/users_list.json") as file:
        validate(body, schema=json.loads(file.read()))


def test_create_user_fail():
    name = "Anton"
    job = "QA"
    response = requests.post(f"{base_url}users", json={
        "name": name,
        "job": job
    })
    assert response.status_code == 201
    assert response.json()["name"] == job
    assert response.json()["job"] == name


def test_get_error_status_code():
    response = requests.get(f"{base_url}users/2")
    assert response.status_code == 400


def test_get_invalid_user():
    response = requests.get(f"{base_url}users/2")
    body = response.json()
    with open("files/only_user.json") as file:
        validate(body, schema=json.loads(file.read()))
