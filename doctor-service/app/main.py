from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient, ReturnDocument
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Doctor Service",
    version="1.0.0",
    root_path="/doctors"
)

mongo_url = os.getenv("MONGO_URL")
if not mongo_url:
    raise ValueError("MONGO_URL is not set in .env")

client = MongoClient(mongo_url)
db = client["hospital_db"]

doctors_collection = db["doctors"]
counters_collection = db["counters"]


class DoctorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    specialization: str = Field(..., min_length=2, max_length=100)


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
    return {"message": "Doctor Service is running"}


@app.get("/")
def get_doctors():
    return list(doctors_collection.find({}, {"_id": 0}))


@app.get("/{doctor_id}")
def get_doctor(doctor_id: int):
    doctor = doctors_collection.find_one({"id": doctor_id}, {"_id": 0})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@app.post("/")
def create_doctor(doctor: DoctorCreate):
    new_id = get_next_sequence("doctor_id")

    new_doctor = {
        "id": new_id,
        "name": doctor.name,
        "specialization": doctor.specialization
    }

    doctors_collection.insert_one(new_doctor)
    new_doctor.pop("_id", None)
    return new_doctor