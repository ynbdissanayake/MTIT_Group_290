from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from pymongo import MongoClient, ReturnDocument
from dotenv import load_dotenv
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
    date_of_birth: date
    contact: str

    @field_validator("contact")
    @classmethod
    def validate_contact(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")
        if len(value) != 10:
            raise ValueError("Mobile number must be exactly 10 digits")
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value


def calculate_age(date_of_birth: date) -> int:
    today = date.today()
    age = today.year - date_of_birth.year

    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1

    return age


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
    age = calculate_age(patient.date_of_birth)

    new_patient = {
        "id": new_id,
        "name": patient.name,
        "date_of_birth": str(patient.date_of_birth),
        "age": age,
        "contact": patient.contact
    }

    patients_collection.insert_one(new_patient)

    new_patient.pop("_id", None)
    return new_patient