import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from src.locations import area_coordinates

app = FastAPI()
model = joblib.load("model/model.pkl")

class InputData(BaseModel):
    pickup_area: str
    dropoff_area: str
    passenger_count: int
    hour: int
    day: int

@app.post("/predict")
def predict(data: InputData):
    if data.pickup_area not in area_coordinates or data.dropoff_area not in area_coordinates:
        return {"error": "Invalid pickup or dropoff area"}

    pickup = area_coordinates[data.pickup_area]
    dropoff = area_coordinates[data.dropoff_area]

    features = np.array([[pickup[0], pickup[1],
                          dropoff[0], dropoff[1],
                          data.passenger_count, data.hour, data.day]])

    prediction = model.predict(features)[0]
    return {
        "fare_amount": round(prediction, 2),
        "pickup_coords": pickup,
        "dropoff_coords": dropoff
    }
