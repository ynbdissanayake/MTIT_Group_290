from fastapi import FastAPI
from dotenv import load_dotenv
from pymongo import MongoClient
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