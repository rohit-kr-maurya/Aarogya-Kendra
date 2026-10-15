import os
import random
import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from google import genai
from google.genai import types

import models
import schemas
from database import engine, get_db

# Load environment variables
load_dotenv()

# Initialize Database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aarogya Kendra Clinical API", version="1.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GenAI Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Pydantic schema for diagnose endpoint
class DiagnoseRequest(BaseModel):
    issue: str
    complaints: str

@app.get("/")
def root():
    return {"status": "Online", "service": "Aarogya-Kendra Backend"}

# 1. Register Patient Endpoint
@app.post("/api/v1/patients", response_model=schemas.PatientResponse)
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Patient).filter(models.Patient.mobile == payload.mobile).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient with this mobile already exists")

    patient_id = f"P-{datetime.datetime.now().strftime('%y%m')}-{random.randint(1000, 9999)}"
    
    new_patient = models.Patient(
        id=patient_id,
        name=payload.name,
        mobile=payload.mobile,
        age=payload.age,
        gender=payload.gender,
        city=payload.city
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# 2. Record Visit Endpoint
@app.post("/api/v1/visits", response_model=schemas.VisitResponse)
def create_visit(payload: schemas.VisitCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient ID not found")

    visit_id = f"V-{datetime.datetime.now().strftime('%y%m')}-{random.randint(1000, 9999)}"
    new_visit = models.Visit(
        id=visit_id,
        patient_id=payload.patient_id,
        issue=payload.issue,
        complaints=payload.complaints,
        points=payload.points,
        advice=payload.advice,
        next_follow_up=payload.next_follow_up
    )
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit

# 3. Get Patient Profile with all Visits
@app.get("/api/v1/patients/{patient_id}")
def get_patient_profile(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    visits = db.query(models.Visit).filter(models.Visit.patient_id == patient_id).all()
    return {
        "patient": patient,
        "visits": visits
    }

# 4. Clinical AI Diagnostic Endpoint (Dual-Tier Failover)
@app.post("/api/v1/diagnose")
def get_diagnosis(payload: DiagnoseRequest):
    prompt = f"""
    You are an expert Acupressure & Natural Health Assistant.
    Issue: {payload.issue}
    Complaints: {payload.complaints}

    Provide response in strict JSON with two keys:
    - points: comma-separated recommended acupressure points
    - advice: brief dietary and lifestyle precautions
    """
    try:
        # Primary tier: Fast & Low Latency
        res = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return {"source": "primary", "result": res.text}
    except Exception:
        # Fallback tier: Resilient Failover
        res = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return {"source": "fallback", "result": res.text}