from fastapi import FastAPI
from starlette.responses import RedirectResponse
import os

app = FastAPI()
# import all the routes
from app.routers.people import router as people
app.include_router(people, prefix="/people")

from app.routers.users import router as users
app.include_router(users, prefix="/users")

from app.routers.misc import router as misc
app.include_router(misc)

from app.routers.ticTacToe import router as ticTacToe
app.include_router(ticTacToe, prefix="/tictactoe")


# redirect / -> /docs
@app.get("/", include_in_schema=False, tags=["misc"])
async def root():
	return RedirectResponse(url='/docs')