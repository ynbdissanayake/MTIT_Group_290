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
