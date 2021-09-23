from fastapi import FastAPI
import os
import pymongo
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId

app = FastAPI()
DB_LOGIN = os.environ.get('DB_LOGIN')
DB_PASSWORD  = os.environ.get('DB_PASSWORD')
cluster = MongoClient(f"mongodb+srv://{DB_LOGIN}:{DB_PASSWORD}@api-hryszko-dev.eqopn.mongodb.net/api-hryszko.dev?retryWrites=true&w=majority")
db = cluster["api-hryszko-dev"]

class Person(BaseModel):
	name: str
	surname: str
	age: int

@app.get("/")
async def root():
    return {"message": "Hello fwend!"}

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