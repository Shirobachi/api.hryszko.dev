from fastapi.testclient import TestClient
from ..main import app
from random import randint

client = TestClient(app)

# == ADD PERSON ==
def test_add_person_200_1():
	r = client.post('/people/', json={ "name": "Simon", "surname": "Hryszko", "age": 24 })

	# Remove the person from the database
	client.delete('/people/' + str(r.json()['id']))

	assert r.status_code == 200

def test_add_person_200_2():
	r = client.post('/people/', json={ "name": "Łukasz", "surname": "Fidłowski", "age": 22 })

	# Remove the person from the database
	client.delete('/people/' + str(r.json()['id']))

	assert r.status_code == 200

def test_add_person_422_1():
	r = client.post('/people/', json={ 
	"name": "A", # Good validation: len(name) > 3 and len(name) < 20
	"surname": "A", # Good validation: len(surname) > 3 and len(surname) < 20
	"age": 24
	})

	assert r.status_code == 422

def test_add_person_422_2():
	r = client.post('/people/', json={ 
	"name": "A" * 21, # Good validation: len(name) > 3 and len(name) < 20
	"surname": "A" * 21, # Good validation: len(surname) > 3 and len(surname) < 20
	"age": 24
	})

	assert r.status_code == 422

def test_add_person_422_3():
	r = client.post('/people/', json={ 
	"name": "Simon1", # Good validation: name.isalpha() == True
	"surname": "Hryszko1", # Good validation: surname.isalpha() == True
	"age": 24
	})

	assert r.status_code == 422

def test_add_person_422_4():
	r = client.post('/people/', json={ 
	"name": "Simon!", # Good validation: name.isalpha() == True
	"surname": "Hryszko!", # Good validation: surname.isalpha() == True
	"age": 24
	})

	assert r.status_code == 422

def test_add_person_422_5():
	r = client.post('/people/', json={ 
	"name": "!@#%$#*((", # Good validation: name.isalpha() == True
	"surname": "!@#%$#*((", # Good validation: surname.isalpha() == True
	"age": 24
	})

	assert r.status_code == 422

def test_add_person_422_6():
	r = client.post('/people/', json={ 
	"name": "Simon",
	"surname": "Hryszko",
	"age": 0 # Good validation: age > 0 and age <= 122
	})

	assert r.status_code == 422

def test_add_person_422_7():
	r = client.post('/people/', json={ 
	"name": "Simon",
	"surname": "Hryszko",
	"age": -666 # Good validation: age > 0 and age <= 122
	})

	assert r.status_code == 422

def test_add_person_422_8():
	r = client.post('/people/', json={ 
	"name": "Simon",
	"surname": "Hryszko",
	"age": 666 # Good validation: age > 0 and age <= 122
	})

	assert r.status_code == 422

def test_add_person_422_9():
	r = client.post('/people/', json={ 
	"name": "Simon",
	"surname": "Hryszko",
	"age": "666" # Good validation: age is int
	})

	assert r.status_code == 422

# == READ PERSON ==
def test_read_person_200_1():
	# Add a person to the database
	tmp = client.post('/people/', json={ "name": "Simon", "surname": "Hryszko", "age": 24 })

	r = client.get('/people/' + str(tmp.json()['id']))

	# Remove the person from the database
	client.delete('/people/' + str(r.json()['id']))

	assert r.status_code == 200

def test_read_person_400_1():
	r = client.get('/people/' + "0" * 5) #Good validation: id.isValid() == True | 25 bytes

	assert r.status_code == 400

def test_read_person_404_1():
	# Add a person and remove them to the database
	tmp = client.post('/people/', json={ "name": "Simon", "surname": "Hryszko", "age": 24 })
	client.delete('/people/' + str(tmp.json()['id']))

	r = client.get('/people/' + str(tmp.json()['id'])) #Good validation: id.isValid() == True | 25 bytes

	assert r.status_code == 404

# == DELETE PERSON ==

def test_delete_person_200_1():
	tmp = client.post('/people/', json={ "name": "Simon", "surname": "Hryszko", "age": 24 })
	r = client.delete('/people/' + str(tmp.json()['id']))

	assert r.status_code == 200

def test_delete_person_400_1():
	r = client.delete('/people/' + "0" * 5) #Good validation: id.isValid() == True | 25 bytes

	assert r.status_code == 400

def test_delete_person_404_1():
	# Add a person and remove them to the database
	tmp = client.post('/people/', json={ "name": "Simon", "surname": "Hryszko", "age": 24 })
	client.delete('/people/' + str(tmp.json()['id']))

	r = client.delete('/people/' + str(tmp.json()['id'])) #Good validation: id.isValid() == True | 25 bytes

	assert r.status_code == 404


# == UPDATE PERSON (put) ==
def test_update_person_put_200_1():
	tmp = client.post('/people/', json={ "name": "Simon", "surname": "Hryszko", "age": 24 })
	new_json = { "name": "Jacob", "surname": "Smith", "age": 48 }
	r = client.put('/people/' + str(tmp.json()['id']), json=new_json)

	# Remove the person from the database
	client.delete('/people/' + str(r.json()['id']))

	assert r.status_code == 200

# == UPDATE PERSON (patch) ==
def test_update_person_patch_200_1():
	tmp = client.post('/people/', json={ "name": "Simon", "surname": "Hryszko", "age": 24 })
	new_json = { "name": "Jacob", "age": 48 }
	r = client.patch('/people/' + str(tmp.json()['id']), json=new_json)

	# Remove the person from the database
	client.delete('/people/' + str(r.json()['id']))

	assert r.status_code == 200

# == UPDATE PERSON (patch) ==
def test_update_person_patch_200_2():
	tmp = client.post('/people/', json={ "name": "Simon", "surname": "Hryszko", "age": 24 })
	new_json = { "name": "Jacob","surname": "smith", "age": 48 }
	r = client.patch('/people/' + str(tmp.json()['id']), json=new_json)

	# Remove the person from the database
	client.delete('/people/' + str(r.json()['id']))

	assert r.status_code == 200

# == GET ALL PEOPLE ==

def test_get_all_people_200_1():
	r = client.get('/people/')

	assert r.status_code == 200