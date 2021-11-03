from fastapi import APIRouter
from app.common import *

from pydantic import BaseModel
from typing import List, Optional
from bson.objectid import ObjectId

router = APIRouter()


class Person(BaseModel):
	id: Optional[str]
	name: Optional[str]
	surname: Optional[str]
	age: Optional[int]


# Create
@router.post("/", tags=["people"])
async def add_person(person: Person):
	collection = db["people"]
	collection.insert_one(person.dict())

	return person

# Read all
@router.get("/", response_model=List[Person], tags=["people"])
def get_all_people():
	collection = db["people"]
	collection = collection.find()
	collection = list(collection)

	# Convert _id to str as id
	for person in collection:
		person['id'] = str(person['_id'])
		
	return collection

# Read one
@router.get("/{id}", response_model=Person, tags=["people"])
def get_person(id: str):
	collection = db["people"]
	collection = collection.find_one({"_id": ObjectId(id)})

	return collection

# Update (put)
@router.put("/{id}", tags=["people"])
def update_person(id: str, person: Person):
	collection = db["people"]
	collection.update_one({"_id": ObjectId(id)}, {"$set": person.dict()})

	return person

# Update (patch)
@router.patch("/{id}" , response_model=Person, tags=["people"])
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
@router.delete("/{id}", tags=["people"])
def remove_person(id: str):
	collection = db["people"]
	collection.delete_one({"_id": ObjectId(id)})

	return {"message": "Person deleted"}