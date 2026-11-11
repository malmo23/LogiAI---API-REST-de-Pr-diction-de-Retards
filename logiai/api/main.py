"""L'API LogiAI : python -m uvicorn logiai.api.main:app --reload"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from logiai import config
from logiai.api.schemas import Livraison, PredictionOut
from logiai.predict import Predictor

state: dict = {}  # contient le "predictor" une fois le modèle chargé


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Exécuté UNE fois, au démarrage du serveur (pas à chaque requête)
    if config.MODEL_PATH.exists():
        state["predictor"] = Predictor(config.MODEL_PATH)
    yield
    state.clear()


app = FastAPI(
    title="LogiAI",
    version="1.1.0",
    description="Prédit le risque de retard d'une livraison.",
    lifespan=lifespan,
)

# Autoriser les origines locales (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": "predictor" in state,
        "auth_configured": bool(getattr(config, "API_KEY", None) and getattr(config, "ADMIN_KEY", None)),
    }


@app.post("/v1/predict", response_model=PredictionOut)
def predict(livraison: Livraison):
    predictor = state.get("predictor")
    if predictor is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return PredictionOut(**predictor.predict(livraison.model_dump()))
