"""
Main file for the FastAPI application
"""

from fastapi import FastAPI, status

from app.routes.stories import router as stories_router
from app.routes.dialogs import router as dialogs_router
from app.routes.generate import router as generate_router

app = FastAPI(
	title="Narrify | Generation API",
	version="1.0.0"
)


@app.get("/", status_code=status.HTTP_200_OK)
async def hello_world():
	"""
	Root route
	"""

	return "Hello World"


app.include_router(stories_router, prefix="/stories")
app.include_router(dialogs_router, prefix="/dialogs")
app.include_router(generate_router, prefix="/generate")

if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="0.0.0.0", port=8001)
