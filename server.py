from fastapi import FastAPI, Body
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime

class HealthData(BaseModel):
    heart_rate: int
    oximeter_value: int
    temperature: float
    steps_taken: int
    amount_of_sleep: float
    current_time: datetime = datetime.now()

app = FastAPI()

client = MongoClient("mongodb://localhost:27017")
db = client["thisMain"]
health_data_collection = db["health_data"]

@app.post("/health-data")
async def create_health_data(health_data: HealthData = Body(...)):
    """Create a new health data document in MongoDB."""
    
    health_data_collection.insert_one(health_data.dict())

    return {"message": "Health data saved successfully!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)