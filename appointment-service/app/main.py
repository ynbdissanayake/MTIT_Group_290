from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient, ReturnDocument
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


def get_next_sequence(sequence_name: str) -> int:
    counter = counters_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return counter["sequence_value"]


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


@app.post("/")
def create_appointment(appointment: AppointmentCreate):
    patient = patients_collection.find_one({"id": appointment.patient_id})
    if not patient:
        raise HTTPException(
            status_code=400,
            detail=f"Patient with id {appointment.patient_id} does not exist"
        )

    doctor = doctors_collection.find_one({"id": appointment.doctor_id})
    if not doctor:
        raise HTTPException(
            status_code=400,
            detail=f"Doctor with id {appointment.doctor_id} does not exist"
        )

    new_id = get_next_sequence("appointment_id")

    new_appointment = {
        "id": new_id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "appointment_date": appointment.appointment_date,
        "status": appointment.status
    }

    appointments_collection.insert_one(new_appointment)
    new_appointment.pop("_id", None)

    return new_appointment