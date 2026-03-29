from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient, ReturnDocument
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Billing Service",
    version="1.0.0",
    root_path="/bills"
)

mongo_url = os.getenv("MONGO_URL")
if not mongo_url:
    raise ValueError("MONGO_URL is not set in .env")

client = MongoClient(mongo_url)
db = client["hospital_db"]

bills_collection = db["bills"]
appointments_collection = db["appointments"]
counters_collection = db["counters"]
class BillCreate(BaseModel):
    appointment_id: int
    amount: float = Field(..., gt=0)
    payment_status: str = Field(..., min_length=2, max_length=50)


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
    return {"message": "Billing Service is running"}


@app.get("/")
def get_bills():
    return list(bills_collection.find({}, {"_id": 0}))


@app.get("/{bill_id}")
def get_bill(bill_id: int):
    bill = bills_collection.find_one({"id": bill_id}, {"_id": 0})
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill

