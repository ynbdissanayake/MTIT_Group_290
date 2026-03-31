from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
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
    name: str
    specialization: str


@app.get("/health")
def health():
    return {"message": "Doctor Service is running"}


@app.get("/")
def get_doctors():
    return list(doctors_collection.find({}, {"_id": 0}))