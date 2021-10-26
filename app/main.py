import jwt
from fastapi import FastAPI, HTTPException
import os
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from bson.objectid import ObjectId
from starlette.responses import RedirectResponse
from werkzeug.security import generate_password_hash, check_password_hash


DB_LOGIN = os.environ.get('DB_LOGIN')
DB_PASSWORD  = os.environ.get('DB_PASSWORD')
JWT_SECRET_KEY  = os.environ.get('JWT_SECRET_KEY')

cluster = MongoClient(f"mongodb+srv://{DB_LOGIN}:{DB_PASSWORD}@api-hryszko-dev.eqopn.mongodb.net/api-hryszko.dev?retryWrites=true&w=majority")
db = cluster["api-hryszko-dev"]

app = FastAPI()

# <<>><<>><<>><<>> MISC <<>><<>><<>><<>>

@app.get("/", include_in_schema=False)
async def root():
	return RedirectResponse(url='/docs')

@app.get("/is_even/{number}")
async def is_even(number: int):
	return {"number": number, "is_even": number % 2 == 0}

@app.get("/about")
async def about():
	return {
		"Author": "Simon Hryszko", 
		"Email": "simon@hryszko.dev",
		"Github": "shirobachi",
		"Description": "This is official hryszko.dev API" 
	}


# <<>><<>><<>><<>> PERSON <<>><<>><<>><<>>

class Person(BaseModel):
	id: Optional[str]
	name: Optional[str]
	surname: Optional[str]
	age: Optional[int]


# Create
@app.post("/people")
async def add_person(person: Person):
	collection = db["people"]
	collection.insert_one(person.dict())

	return person

# Read all
@app.get("/people", response_model=List[Person])
def get_all_people():
	collection = db["people"]
	collection = collection.find()
	collection = list(collection)

	# Convert _id to str as id
	for person in collection:
		person['id'] = str(person['_id'])
		
	return collection

# Read one
@app.get("/people/{id}", response_model=Person)
def get_person(id: str):
	collection = db["people"]
	collection = collection.find_one({"_id": ObjectId(id)})

	return collection

# Update (put)
@app.put("/people/{id}")
def update_person(id: str, person: Person):
	collection = db["people"]
	collection.update_one({"_id": ObjectId(id)}, {"$set": person.dict()})

	return person

# Update (patch)
@app.patch("/people/{id}" , response_model=Person)
def update_person(id: str, person: Person):
	server_person = get_person(id)

	# copy person to server_person
	for key, value in person.dict().items():
		if value != None:
			server_person[key] = value

	# update server_person
	collection = db["people"]
	collection.update_one({"_id": ObjectId(id)}, {"$set": server_person})

	return server_person

# Remove 
@app.delete("/people/{id}")
def remove_person(id: str):
	collection = db["people"]
	collection.delete_one({"_id": ObjectId(id)})

	return {"message": "Person deleted"}


# <<>><<>><<>><<>> USER <<>><<>><<>><<>>

class User(BaseModel):
	login: str
	password: str


# Register new person
@app.post("/users")
async def register(user: User):
	Collection = db["users"]
	# TODO: validation (password:tooShort|tooLong)

	# VALIDATION - LOGIN
	# Check if login has special chars
	print (user.login, user.login.isalnum())

	if not user.login.isalnum():
		raise HTTPException(
            status_code=400,
            detail="Login has special chars",
        )

	# if login not b/w 3-20 chars
	if len(user.login) < 3 or len(user.login) > 20:
		raise HTTPException(
            status_code=400,
            detail="Login must be between 3 and 20 characters",
        )

	# Check if login already exist
	if Collection.find_one({"login": user.login}):
		raise HTTPException(
            status_code=400,
            detail="Login has special chars",
        )

	# VALIDATION - PASSWORD
	# check if password has at least one number
	if not any(char.isdigit() for char in user.password):
		raise HTTPException(
            status_code=400,
            detail="Password must contain at least one number",
        )

	# check if password has at least one uppercase letter
	if not any(char.isupper() for char in user.password):
		raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter",
        )

	# check if password is at least 8 chars long and not more than 100
	if len(user.password) < 8 or len(user.password) > 100:
		raise HTTPException(
            status_code=400,
            detail="Password must be between 8 and 100 characters",
        )

	user.password = generate_password_hash(user.password)
	Collection.insert_one(user.dict())

	return {
		"message": "User created"
	}

# Generate token JWT
@app.post("/token")
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
		token = jwt.encode(
			{"id": id}, 
			JWT_SECRET_KEY,
			algorithm="HS256"
		)

		return {
			"token": token
		}


# verify token
@app.get("/token/{token}")
async def verify_token(token: str):

	try:
		r = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256", ])
		r = r['id']
		print(r)

		Collection = db["users"]
		Collection = Collection.find_one({"_id": ObjectId(r)}, {'_id': 0})
		# unset collection.password
		Collection.pop('password')

		return Collection
	except:
		raise HTTPException(
            status_code=401,
            detail="Token invalid!",
        )
