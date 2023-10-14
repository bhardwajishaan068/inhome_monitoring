from fastapi import FastAPI, Body
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import twilio

def emergency_call():
  client = twilio.rest.Client("USbcae142571787ec72b55689abe44f782", )
  doct_phone = "DOCTOR'S PHONE" #Replace with docs phone number

  call = client.calls.create(
      url = "https://twimlets.com/holdmusic?Digits=9"
      to = doct_phone
      from_ = "PATIENT's NUMBER" #Replace with mobile number
)


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
    """Create a new health data document in MongoDB and make an SOS call if the conditions are met."""

    health_data_collection.insert_one(health_data.dict())

    # Check if the alert conditions are met
    if health_data.temperature < 35 or health_data.temperature > 39 or health_data.heart_rate < 75:
        # Make an emergency call to the doctor
        emergency_call()

    return {"message": "Health data saved successfully!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
