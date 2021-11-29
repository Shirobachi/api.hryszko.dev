from fastapi import APIRouter, HTTPException
from app.common import *

from pydantic import BaseModel, Field
from typing import List
from bson.objectid import ObjectId

import random
from datetime import datetime
from datetime import timedelta

from math import floor

router = APIRouter()


#model for the request body
class TicTacToe(BaseModel):
	code: int = Field(lenght=4)
	board: List[List[int]]
	# 0 - 'O', 1 - 'X'
	player: int
	winner: int = None


async def get_all_games():
	collection = db['ticTacToe']
	collection = collection.find({}, {'_id': 0})
	collection = list(collection)

	return collection


def remove_old_games():
	collection = db['ticTacToe']

	calcDate = lambda hours: format(floor((datetime.utcnow() - timedelta(hours=hours)).timestamp()), 'x') + "0" * 16

	# remove finished games and made in before now - 1hour
	collection.delete_many({'_id': {'$lt': ObjectId(calcDate(1))}, 'winner': {'$ne': None}})

	# remove not finished games and made in before now - 1day
	collection.delete_many({'_id': {'$lt': ObjectId(calcDate(24))}, 'winner': {'$eq': None}})


# New game
@router.post("/", tags=["ticTacToe"], response_model=TicTacToe)
async def new_game():
	codes = [game['code'] for game in await get_all_games()]

	# remove old games
	remove_old_games()

	# generate code
	if len(codes) < 9999-1000:
		code = None
		while code in codes or code is None:
			code = random.randint(1000, 9999)
	else:
		raise HTTPException(status_code=400, detail="No more games available, please try again later!")

	code = random.randint(1000, 9999)
	board = TicTacToe(code=code, board=[[-1] * 3] * 3, player=1)

	Collection = db["ticTacToe"]
	Collection.insert_one(board.dict())

	return board


# input: board like [[][][]]
# output: -1 when draw, None when game in progres, 0/1 when player 0/1
def check_winner(board):
	winner = ""

	for row in board:
		if all(row[0] != -1 and row[i] == row[i+1] for i in range(0, len(row)-1)):
			return row[0]
	if winner == "":
		for col in range(len(board[0])):
			if all(board[0][col] != -1 and board[i][col] == board[i+1][col] for i in range(len(board)-1)):
				return board[0][col]
	if winner == "":
		if all(board[0][0] != -1 and board[i][i] == board[i + 1][i + 1] for i in range(len(board) - 1)):
			return board[0][0]
	if winner == "":
		if all(board[0][len(board) -1] != -1 and board[i][len(board) - 1 - i] == board[i + 1][len(board) - 1 - i - 1] for i in range(len(board) - 1)):
			return board[0][len(board) - 1]
	if not any(-1 in row for row in board):
		return -1
	if winner == "":
		return None


# Get game state
@router.get("/{code}", tags=["ticTacToe"], )
async def get_game(code: int):
	Collection = db["ticTacToe"]
	obj = Collection.find_one({'code': code})

	if obj is None:
		raise HTTPException(status_code=404, detail="Game not found")

	return TicTacToe(**obj)


# Add move
@router.post("/{code}/{position}", tags=["ticTacToe"], response_model=TicTacToe)
async def add_move(code: int, position: int):
	board = await get_game(code)

	if check_winner(board.board) != None:
		raise HTTPException(status_code=400, detail="Game is over")
	if position < 0 or position > 8:
		raise HTTPException(status_code=400, detail="Invalid position")
	if board.board[position // 3][position % 3] != -1:
		raise HTTPException(status_code=400, detail="Field is not empty")

	board.board[position // 3][position % 3] = board.player
	board.player = 1 - board.player
	board.winner = check_winner(board.board)

	Collection = db["ticTacToe"]
	Collection.update_one({'code': code}, {'$set': board.dict()})

	return board
