from fastapi.testclient import TestClient
from ..main import app
from random import randint

client = TestClient(app)


# == REGISTER USER ==

def test_register_200_1():
	r = client.post('/users/', json={ "login": "ogapOuygXvHnPtFaCPUo", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"})
	client.delete('/users/', json={ "login": "ogapOuygXvHnPtFaCPUo", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"})

	assert r.status_code == 200


def test_register_200_2():
	r = client.post('/users/', json={ "login": "AktIkGSAj4oVYLbHVfrf", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"})
	client.delete('/users/', json={ "login": "AktIkGSAj4oVYLbHVfrf", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"})

	assert r.status_code == 200


def test_register_422_1():
	json = { "login": "NMMbqEzJfAyglSyGHEXM", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"}

	client.post('/users/', json=json)
	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	# user already exists
	assert r.status_code == 422


def test_register_422_2():
	json = { "login": "kVmuYUYdsnBwAGYSzOIX", "password": "aA1"} # password too short

	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 422


def test_register_422_3():
	json = { "login": "kVmuYUYdsnBwAGYSzOIX", "password": "aA1" * 66} # password too looong

	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 422


def test_register_422_4():
	json = { "login": "kVmuYUYdsnBwAGYSzOIX", "password": "aA" * 10} # password not containt digits

	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 422


def test_register_422_5():
	json = { "login": "kVmuYUYdsnBwAGYSzOIX", "password": "a1" * 10} # password not containt capital letters

	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 422


def test_register_422_6():
	json = { "login": "kVmuYUYdsnBwAGYSzOIX", "password": "1A" * 10} # password not containt lowercase letters

	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 422


def test_register_422_7():
	json = { "login": "kVmuYUYdsnBwAGYSzOIX", "password": "aA!" * 10} # password containt special chars

	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 422


def test_register_422_8():
	json = { "login": "A", "password": "aA1" * 10} # Login is too short

	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 422
	

def test_register_422_9():
	json = { "login": "A" * 25, "password": "aA1" * 10} # Login is too loong

	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 422
	

def test_register_422_10():
	json = { "login": "A@" * 2, "password": "aA1" * 10} # Login contains invalid chars

	r = client.post('/users/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 422


# == DELETE USER ==

def test_delete_200_1():
	json = { "login": "TccgJAmlPTqxEwGlbUye", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"}
	client.post('/users/', json=json)

	r = client.delete('/users/', json=json)

	assert r.status_code == 200


def test_delete_401_1():
	json = { "login": "TccgJAmlPTqxEwGlbUye", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"}

	tmp = client.post('/users/', json=json)
	r = client.delete('/users/', json={ "login": "TccgJAmlPTqxEwGlbUye", "password": "aS1aS1aS1aS1aS1"})

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 401

# == GENERATE TOKEN ==


def test_generate_token_200_1():
	json = { "login": "TccgJAmlPTqxEwGlbUye", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"}
	client.post('/users/', json=json)

	r = client.post('/users/token/', json=json)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 200

def test_generate_token_401_1():
	json = { "login": "TccgJAmlPTqxEwGlbUye", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"}
	client.post('/users/', json=json)

	r = client.post('/users/token/', json={ "login": "TccgJAmlPTqxEwGlbUye", "password": "aS1aS1aS1aS1aS1"})

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 401


# == VERIFY TOKEN ==

def test_verify_token_200_1():
	json = { "login": "TccgJAmlPTqxEwGlbUye", "password": "KvRgVa6bhDyAzmondLosD0YIdrkEiirqN4mPP5Zytcn8W57cXAlfUwMqn2S9zUC7"}
	client.post('/users/', json=json)

	token = client.post('/users/token/', json=json).json()['token']
	r = client.get('/users/token/' + token)

	# delete user
	client.delete('/users/', json=json)

	assert r.status_code == 200
	assert r.json()['login'] == json['login']

def test_verify_token_401_1():

	assert client.get('/users/token/ey0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYxOWZiNzhhMGRiZjMxYTcxZjYxOGRjYyJ9.lj9OKBaZBxWRXKQoDlLWUHbIlvXt5a4bYo-AKgKngV0').status_code == 401