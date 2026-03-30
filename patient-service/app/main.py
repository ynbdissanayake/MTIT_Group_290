from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Patient Service",
    version="1.0.0",
    root_path="/patients"
)