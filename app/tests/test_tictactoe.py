from fastapi.testclient import TestClient
from ..main import app
from random import randint

client = TestClient(app)

# == NEW GAME ==
def test_new_game_200_1():
	response = client.post('/tictactoe/')

	assert response.status_code == 200
	assert response.json()['winner'] == None


# == GAME STATE ==
def test_game_state_200_1():
	response = client.post('/tictactoe/')
	response = client.get('/tictactoe/' + str(response.json()['code']))

	assert response.status_code == 200


def test_game_state_422_2():
	r = client.get('/tictactoe/' + "asd")

	assert r.status_code == 422


# == MAKE MOVE ==
def test_make_move_422_1():
	response = client.post('/tictactoe/')
	response = client.put('/tictactoe/' + str(response.json()['code']) + "/dasd")

	assert response.status_code == 422


def test_draw_1_200_1():
	tmp = client.post('/tictactoe/')

	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/4")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/0")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/1")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/7")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/3")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/5")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/6")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/2")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/8")

	assert response.status_code == 200
	assert response.json()['winner'] == -1


def test_win_row_1_200_1():
	tmp = client.post('/tictactoe/')

	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/0")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/3")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/1")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/4")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/2")

	print(response.json())

	assert response.status_code == 200
	assert response.json()['winner'] == 1


def test_win_row_2_200_1():
	tmp = client.post('/tictactoe/')

	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/3")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/6")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/4")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/7")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/5")

	print(response.json())

	assert response.status_code == 200
	assert response.json()['winner'] == 1


def test_win_row_3_200_1():
	tmp = client.post('/tictactoe/')

	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/6")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/4")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/7")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/5")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/8")

	print(response.json())

	assert response.status_code == 200
	assert response.json()['winner'] == 1


def test_win_col_1_200_1():
	tmp = client.post('/tictactoe/')

	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/0")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/1")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/3")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/2")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/6")

	print(response.json())

	assert response.status_code == 200
	assert response.json()['winner'] == 1


def test_win_col_2_200_1():
	tmp = client.post('/tictactoe/')

	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/1")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/0")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/4")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/2")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/7")

	print(response.json())

	assert response.status_code == 200
	assert response.json()['winner'] == 1


def test_win_col_3_200_1():
	tmp = client.post('/tictactoe/')

	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/2")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/4")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/5")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/1")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/8")

	print(response.json())

	assert response.status_code == 200
	assert response.json()['winner'] == 1


def test_win_diagonal_1_200_1():
	tmp = client.post('/tictactoe/')

	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/0")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/1")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/4")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/3")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/8")

	print(response.json())

	assert response.status_code == 200
	assert response.json()['winner'] == 1


def test_win_diagonal_2_200_1():
	tmp = client.post('/tictactoe/')

	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/2")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/1")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/4")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/7")
	response = client.put('/tictactoe/' + str(tmp.json()['code']) + "/6")

	print(response.json())

	assert response.status_code == 200
	assert response.json()['winner'] == 1