# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Charger le modèle
model = joblib.load("model_air_quality.joblib")

app = FastAPI(title="API Prédiction Qualité de l'air")

# Schéma de la requête
class SensorData(BaseModel):
    co2: float
    pm25: float
    temp: float
    hum: float

@app.get("/")
def read_root():
    return {"status": "API is running", "endpoint": "/predict"}


@app.post("/predict")
def predict(data: SensorData):
    features = np.array([[data.co2, data.pm25, data.temp, data.hum]])
    prediction = model.predict(features)[0]
    # On peut renvoyer la probabilité aussi si on veut
    proba = model.predict_proba(features)[0].tolist()
    return {
        "prediction": int(prediction),
        "probability": proba
    }
