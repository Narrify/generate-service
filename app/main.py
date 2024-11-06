import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.clients.mongo import insert_tracking
from app.routes.generate import router as generate_router
from app.routes.prompts import router as prompts_router
from time import time

app = FastAPI(
    title="Narrify | Generation API",
    description="API for generating stories and dialogues",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8002", "http://127.0.0.1:8002"],  # Allow both localhost and 127.0.0.1
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
async def hello_world():
    startt = time()
    endt = time()

    insert_tracking(
        route="/",
        status_code=200,
        start_date=startt,
        end_date=endt,
        latency=endt - startt,
    )

    return "Hello World"


app.include_router(generate_router, prefix="/generate")
app.include_router(prompts_router, prefix="/prompts")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
