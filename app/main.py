from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello fwend!"}

@app.get("/isEven/{number}")
async def isEven(number: int):
    return {"number": number, "isEven": number % 2 == 0}

@app.get("/about")
async def about():
	return { 	"Author": "Simon Hryszko", 
				"Email": "simon@hryszko.dev",
				"Github": "shirobachi",
				"Description": "This is official hryszko.dev API" }