from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routes.generate import router as generate_router

app = FastAPI(
    title="Narrify | Generation API",
    description="API for generating stories and dialogues",
    version="1.0.0"
)

# Configure CORS to allow access from http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Can add more origins in the list
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/", status_code=status.HTTP_200_OK)
async def hello_world():
    """
    Simple hello world endpoint.
    """
    return "Hello World"

app.include_router(generate_router, prefix="/generate")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
