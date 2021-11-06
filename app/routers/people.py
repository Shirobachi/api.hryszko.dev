from fastapi import APIRouter, HTTPException
from app.common import *

from pydantic import BaseModel
from typing import List, Optional
from bson.objectid import ObjectId

router = APIRouter()


# Models
class Person(BaseModel):
	name: str
	surname: str
	age: int

class PersonOptional(BaseModel):
	name: Optional[str]
	surname: Optional[str]
	age: Optional[int]


class PersonWithID(BaseModel):
	id: str
	name: str
	surname: str
	age: int


# Validateion functions
def validate_name(val):
	if not val.isalpha():  # isAlpha()
		return False
	if len(val) < 3 or len(val) > 20:  # len b/w 3-20
		return False

	return True


def validate_age(val):
	if val <= 0 or val > 122: # len b/w 1-2
		return False

	return True


def validate_id(val):
	if(not ObjectId.is_valid(val)): # if valid id pattern
		return False

	return True

# ============================================================
# Create
@router.post("/", response_model=PersonWithID, tags=["people"])
async def add_person(person: Person):
	# Validation
	if(not validate_name(person.name)):
		raise HTTPException( status_code=400, detail="Incorrect name!", )
	if(not validate_name(person.surname)):
		raise HTTPException( status_code=400, detail="Incorrect surname!", )
	if(not validate_age(person.age)):
		raise HTTPException( status_code=400, detail="Incorrect age!", )

	# make first letter of name uppercase
	person.name = person.name.title()
	person.surname = person.surname.title()

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

	if(not validate_name(person.name)):
		raise HTTPException( status_code=400, detail="Incorrect name!", )
	if(not validate_name(person.surname)):
		raise HTTPException( status_code=400, detail="Incorrect surname!", )
	if(not validate_age(person.age)):
		raise HTTPException( status_code=400, detail="Incorrect age!", )

	# make first letter of name uppercase
	person.name = person.name.title()
	person.surname = person.surname.title()

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

	if(person.name != None and not validate_name(person.name)):
		raise HTTPException( status_code=400, detail="Incorrect name!", )
	if(person.surname != None and not validate_name(person.surname)):
		raise HTTPException( status_code=400, detail="Incorrect surname!", )
	if(person.age != None and not validate_age(person.age)):
		raise HTTPException( status_code=400, detail="Incorrect age!", )


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