from fastapi import FastAPI
import os
import pymongo
from pymongo import MongoClient

app = FastAPI()
DB_LOGIN = os.environ.get('DB_LOGIN')
DB_PASSWORD  = os.environ.get('DB_PASSWORD')
cluster = MongoClient(f"mongodb+srv://{DB_LOGIN}:{DB_PASSWORD}@api-hryszko-dev.eqopn.mongodb.net/api-hryszko.dev?retryWrites=true&w=majority")

@app.get("/")
async def root():
    return {"message": "Hello fwend!"}

@app.get("/isEven/{number}")
async def isEven(number: int):
    return {"number": number, "isEven": number % 2 == 0}

@app.get("/about")
async def about():
	return {
		"Author": "Simon Hryszko", 
		"Email": "simon@hryszko.dev",
		"Github": "shirobachi",
		"Description": "This is official hryszko.dev API" 
	}

@app.post("/people/add")
async def add_person(name: str, surname: str, age: int):
	collection = cluster["api-hryszko-dev"]["people"]

	collection.insert_one({
		"name": name, 
		"surname": surname, 
		"age": age
	})

	return {"message": f"{name} was added"}
