import uvicorn
from fastapi import FastAPI, status, Request
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


from starlette.middleware.base import BaseHTTPMiddleware

# Diccionario para contar las respuestas
response_counts = {"2xx": 0, "4xx": 0, "5xx": 0}


class ResponseCounterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Contar el tipo de respuesta
        status_code = response.status_code
        if 200 <= status_code < 300:
            response_counts["2xx"] += 1
        elif 400 <= status_code < 500:
            response_counts["4xx"] += 1
        elif 500 <= status_code < 600:
            response_counts["5xx"] += 1

        return response


app.add_middleware(ResponseCounterMiddleware)


@app.get("/metrics")
async def get_metrics():
    # Calcular disponibilidad y confiabilidad
    try:
        availability = response_counts["2xx"] / (response_counts["2xx"] + response_counts["5xx"])
    except ZeroDivisionError:
        availability = 1.0  # Considera disponibilidad plena si no hay errores 5xx
    try:
        reliability = response_counts["2xx"] / (response_counts["2xx"] + response_counts["4xx"])
    except ZeroDivisionError:
        reliability = 1.0  # Considera confiabilidad plena si no hay errores 4xx

    return {
        "availability": availability,
        "reliability": reliability,
        "response_counts": response_counts
    }


app.include_router(generate_router, prefix="/generate")
app.include_router(prompts_router, prefix="/prompts")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
