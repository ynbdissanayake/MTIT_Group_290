from fastapi import FastAPI
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