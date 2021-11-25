from fastapi import APIRouter, HTTPException
from app.common import *

from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Optional
from bson.objectid import ObjectId

router = APIRouter()


# Models
class Person(BaseModel):
	name: str
	surname: str
	age: int

	# validate
	@validator('name')
	def validate_name(cls, v):
		if not v.isalpha():
			raise ValueError('Name must be alphabetic')
		if len(v) < 3 or len(v) > 20:
			raise ValueError('Name must be between 3 and 20 characters')

		return v.title()


	@validator('surname')
	def validate_surname(cls, v):
		if not v.isalpha():
			raise ValueError('Surname must be alphabetic')
		if len(v) < 3 or len(v) > 20:
			raise ValueError('Name must be between 3 and 20 characters')

		return v.title()

	
	@validator('age')
	def validate_age(cls, v):
		if v <= 0 or v > 122:
			raise ValueError('Age must be between 1 and 122')

		return v


class PersonOptional(Person):
	name: Optional[str]
	surname: Optional[str]
	age: Optional[int]
	

class PersonWithID(BaseModel):
	id: str
	name: str
	surname: str
	age: int


def validate_id(val):
	if(not ObjectId.is_valid(val)): # if valid id pattern
		return False

	return True

# ============================================================
# Create
@router.post("/", response_model=PersonWithID, tags=["people"])
async def add_person(person: Person):
	# Insert
	collection = db["people"]
	id = collection.save(person.dict())

	return get_person(id)


# Read all
@router.get("/", response_model=List[PersonWithID], tags=["people"])
def get_all_people():
	collection = db["people"]
	collection = collection.find()
	collection = list(collection)

	# Convert _id to str as id
	for person in collection:
		person['id'] = str(person['_id'])

	return collection

# Read one
@router.get("/{id}", response_model=PersonWithID, tags=["people"])
def get_person(id: str):
	# Validation
	if not validate_id(id):
		raise HTTPException( status_code=400, detail="Incorrect id!")

	# Get data
	collection = db["people"]
	collection = collection.find_one({"_id": ObjectId(id)})
	collection['id'] = str(collection['_id'])

	# check if person exist
	if collection is None:
		raise HTTPException( status_code=404, detail="Person not found!", )

	return collection


# Update (put)
@router.put("/{id}",response_model=PersonWithID,  tags=["people"])
def update_person(id: str, person: Person):
	# Validation
	if not validate_id(id):
		raise HTTPException( status_code=400, detail="Incorrect id!", )
	if db["people"].find_one({"_id": ObjectId(id)}) is None:
		raise HTTPException( status_code=404, detail="Person not found!", )

	# Update
	collection = db["people"]
	collection.update_one({"_id": ObjectId(id)}, {"$set": person.dict()})

	return get_person(id)


# Update (patch)
@router.patch("/{id}" ,response_model=PersonWithID, tags=["people"])
def update_person(id: str, person: PersonOptional):
	# Validation
	if not validate_id(id):
		raise HTTPException( status_code=400, detail="Incorrect id!", )
	if db["people"].find_one({"_id": ObjectId(id)}) is None:
		raise HTTPException( status_code=404, detail="Person not found!", )


	# copy person to server_person
	server_person = get_person(id)
	for key, value in person.dict().items():
		if value != None:
			server_person[key] = value

	# update server_person
	collection = db["people"]
	collection.update_one({"_id": ObjectId(id)}, {"$set": server_person})

	return get_person(id)


# Remove 
@router.delete("/{id}", tags=["people"])
def remove_person(id: str):
	# Validation
	if not validate_id(id):
		raise HTTPException( status_code=400, detail="Incorrect id!", )
	if db["people"].find_one({"_id": ObjectId(id)}) is None:
		raise HTTPException( status_code=404, detail="Person not found!", )


	collection = db["people"]
	collection.delete_one({"_id": ObjectId(id)})

	return {"message": "Person deleted"}