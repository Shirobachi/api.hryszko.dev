from fastapi import APIRouter

router = APIRouter()


@router.get("/is_even/{number}", tags=["misc"])
async def is_even(number: int):
	return {"number": number, "is_even": number % 2 == 0}

@router.get("/about", tags=["misc"])
async def about():
	return {
		"Author": "Simon Hryszko", 
		"Email": "simon@hryszko.dev",
		"Github": "shirobachi",
		"Description": "This is official hryszko.dev API" 
	}
