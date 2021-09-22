from fastapi import FastAPI
import os
import pymongo
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()
DB_LOGIN = os.environ.get('DB_LOGIN')
DB_PASSWORD  = os.environ.get('DB_PASSWORD')
cluster = MongoClient(f"mongodb+srv://{DB_LOGIN}:{DB_PASSWORD}@api-hryszko-dev.eqopn.mongodb.net/api-hryszko.dev?retryWrites=true&w=majority")

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

@app.post("/people")
async def add_person(person: Person):
	collection = cluster["api-hryszko-dev"]["people"]

	collection.insert_one(person)

	return {"message": f"{person.name} was added"}

	return {"message": f"{name} was added"}
