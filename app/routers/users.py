from fastapi import APIRouter, HTTPException
from app.common import *

from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional
import jwt

router = APIRouter()

# Models
class User(BaseModel):
	login: str = Field(min_length=3, max_length=20)
	password: str = Field(min_length=8, max_length=100)

	@validator('login')
	def login_is_alphanum(cls, v):
		if not v.isalnum():
			raise ValueError('Login must be alphanumeric')

		return v

	@validator('password')
	def password_is_secure(cls, v):
		if not v.isalnum():
			raise ValueError('Password must be alphanumeric')
		if not any(char.isdigit() for char in v):
			raise ValueError('Password must contain a number')
		if not any(char.isupper() for char in v):
			raise ValueError('Password must contain an upper case letter')
		if not any(char.islower() for char in v):
			raise ValueError('Password must contain an lower case letter')

		return v

class UserNoPass(BaseModel):
	login: str

class Token(BaseModel):
	token: str


# Register new person
@router.post("/", response_model=UserNoPass, tags=["users"])
async def register(user: User):
	# Validation
	if db.users.find_one({'login': user.login}):
		raise HTTPException( status_code=422, detail="Login taken")

	Collection = db["users"]
	user.password = generate_password_hash(user.password)
	Collection.insert_one(user.dict())

	return user


# Delete user
@router.delete("/", tags=["users"])
async def delete(user: User):
	if db["users"].find_one({"login": user.login}) is None:
		raise HTTPException( status_code=404, detail="Account not found!")

	# check password
	if not check_password_hash(db["users"].find_one({"login": user.login})["password"], user.password):
		raise HTTPException( status_code=401, detail="Wrong password!")

	collection = db["users"]
	collection.delete_one({"login": user.login})

	return {"message": "Account deleted!"}


# Generate token JWT
@router.post("/token/", response_model=Token, tags=["users"])
async def login(user: User):
	Collection = db["users"]
	Collection = Collection.find_one({"login": user.login})

	if Collection == None or not (check_password_hash(Collection['password'], user.password)):
		raise HTTPException(
            status_code=401,
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
