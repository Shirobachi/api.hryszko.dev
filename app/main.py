from fastapi import FastAPI
from starlette.responses import RedirectResponse
import os

# import all the routes
from app.routers.people import router as people
from app.routers.users import router as users
from app.routers.misc import router as misc

# run app with routes
app = FastAPI()
app.include_router(people, prefix="/people")
app.include_router(users, prefix="/users")
app.include_router(misc)


# redirect / -> /docs
@app.get("/", include_in_schema=False, tags=["misc"])
async def root():
	return RedirectResponse(url='/docs')