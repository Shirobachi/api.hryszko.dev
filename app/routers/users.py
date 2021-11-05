from fastapi import APIRouter, HTTPException
from app.common import *

from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional
import jwt

router = APIRouter()

# Models
class User(BaseModel):
	login: str
	password: str
class UserNoPass(BaseModel):
	login: str

class Token(BaseModel):
	token: str


# Register new person
@router.post("/", response_model=UserNoPass, tags=["users"])
async def register(user: User):
	Collection = db["users"]
	# TODO: validation (password:tooShort|tooLong)

	# VALIDATION - LOGIN
	# Check if login has special chars
	print (user.login, user.login.isalnum())

	if not user.login.isalnum(): # if login contain a-zA-Z0-9
		raise HTTPException( status_code=400, detail="Login has special chars")
	if len(user.login) < 3 or len(user.login) > 20: # if login not b/w 3-20 chars
		raise HTTPException( status_code=400, detail="Login must be between 3 and 20 characters")
	if Collection.find_one({"login": user.login}): # Check if login already exist
		raise HTTPException( status_code=400, detail="Login taken")
	if not any(char.isdigit() for char in user.password): # check if password has at least one number
		raise HTTPException( status_code=400, detail="Password must contain at least one number")
	if not any(char.isupper() for char in user.password): # check if password has at least one uppercase letter
		raise HTTPException( status_code=400, detail="Password must contain at least one uppercase letter")
	if len(user.password) < 8 or len(user.password) > 100: # check if password is at least 8 chars long and not more than 100
		raise HTTPException( status_code=400, detail="Password must be between 8 and 100 characters")


	user.password = generate_password_hash(user.password)
	Collection.insert_one(user.dict())

	return user


# Generate token JWT
@router.post("/token", response_model=Token, tags=["users"])
async def login(user: User):
	Collection = db["users"]
	Collection = Collection.find_one({"login": user.login})

	if Collection == None or not (check_password_hash(Collection['password'], user.password)):
		raise HTTPException(
            status_code=403,
            detail="Credentials invalid!",
        )
	else:
		id = str(Collection['_id'])

		return {
			"token": jwt.encode(
			{"id": id}, 
			JWT_SECRET_KEY,
			algorithm="HS256"
			)
		}


# verify token
@router.get("/token/{token}", response_model=UserNoPass, tags=["users"])
async def verify_token(token: str):
	try:
		r = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256", ])
		r = r['id']

		Collection = db["users"]
		Collection = Collection.find_one({"_id": ObjectId(r)}, {'_id': 0})

		Collection.pop('password')

		return Collection
	except:
		raise HTTPException(
            status_code=401,
            detail="Token invalid!",
        )
