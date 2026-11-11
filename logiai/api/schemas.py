from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

class Livraison(BaseModel):
    model_config = ConfigDict(extra="forbid")

    distance_km: float = Field(..., ge=1.0, le=1000.0)
    poids_kg: float = Field(..., ge=1.0, le=5000.0)
    heure_depart: float = Field(..., ge=0, le=23)
    pluie_mm: float = Field(..., ge=0.0, le=100.0)
    trafic_index: float = Field(..., ge=0.0, le=10.0)
    nb_arrets: int = Field(..., ge=0, le=20)
    type_vehicule: Literal["camion", "fourgon", "moto", "utilitaire", "velo"] = "camion"

class PredictionOut(BaseModel):
    probabilite_retard: float
    alerte: bool
    seuil: float
    model_version: str
