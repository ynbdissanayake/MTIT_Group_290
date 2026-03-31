from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from pydantic import BaseModel, Field
import os

load_dotenv()

app = FastAPI(
    title="Patient Service",
    version="1.0.0",
    root_path="/patients"
)

mongo_url = os.getenv("MONGO_URL")
if not mongo_url:
    raise ValueError("MONGO_URL is not set in .env")

client = MongoClient(mongo_url)
db = client["hospital_db"]
patients_collection = db["patients"]
counters_collection = db["counters"]


class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=0, le=120)
    contact: str = Field(..., min_length=7, max_length=20)


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
    return {"message": "Patient Service is running"}

@app.get("/")
def get_patients():
    return list(patients_collection.find({}, {"_id": 0}))

@app.get("/{patient_id}")
def get_patient(patient_id: int):
    patient = patients_collection.find_one({"id": patient_id}, {"_id": 0})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/")
def create_patient(patient: PatientCreate):
    new_id = get_next_sequence("patient_id")

    new_patient = {
        "id": new_id,
        "name": patient.name,
        "age": patient.age,
        "contact": patient.contact
    }

    patients_collection.insert_one(new_patient)

    new_patient.pop("_id", None)
    return new_patient