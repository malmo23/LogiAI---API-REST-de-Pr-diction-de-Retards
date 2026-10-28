from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()  # l'application


class Mesure(BaseModel):  # le schéma
    temperature_c: float = Field(ge=-40, le=150)


@app.get("/health")  # la route GET /health
def health():
    return {"status": "ok"}


@app.post("/v1/check")  # la route POST /v1/check
def check(mesure: Mesure):  # mesure : déjà validée
    return {"alerte": mesure.temperature_c > 80}
