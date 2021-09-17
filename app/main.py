from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello fwend!"}

@app.get("/isEven/{number}")
async def isEven(number: int):
    return {"number": number, "isEven": number % 2 == 0}
