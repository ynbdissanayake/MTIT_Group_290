from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Appointment Service",
    version="1.0.0",
    root_path="/appointments"
)

mongo_url = os.getenv("MONGO_URL")
if not mongo_url:
    raise ValueError("MONGO_URL is not set in .env")

client = MongoClient(mongo_url)
db = client["hospital_db"]

appointments_collection = db["appointments"]
patients_collection = db["patients"]
doctors_collection = db["doctors"]
counters_collection = db["counters"]


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str = Field(..., min_length=5, max_length=50)
    status: str = Field(..., min_length=2, max_length=50)


@app.get("/health")
def health():
    return {"message": "Appointment Service is running"}


@app.get("/")
def get_appointments():
    return list(appointments_collection.find({}, {"_id": 0}))


@app.get("/{appointment_id}")
def get_appointment(appointment_id: int):
    appointment = appointments_collection.find_one({"id": appointment_id}, {"_id": 0})
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment