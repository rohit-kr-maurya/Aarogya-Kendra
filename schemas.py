from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

# Patient Schemas
class PatientCreate(BaseModel):
    name: str = Field(..., example="Ramesh Kumar")
    mobile: str = Field(..., min_length=10, max_length=15, example="9876543210")
    age: Optional[int] = Field(None, example=45)
    gender: Optional[str] = Field(None, example="Male")
    city: Optional[str] = Field(None, example="Jaunpur")

class PatientResponse(PatientCreate):
    id: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Visit Schemas
class VisitCreate(BaseModel):
    patient_id: str = Field(..., example="P-1001")
    issue: str = Field(..., example="Cervical & Upper Back Pain")
    complaints: Optional[str] = Field(None, example="Severe stiffness in morning")
    points: Optional[str] = Field(None, example="LI4, GB20, GV14")
    advice: Optional[str] = Field(None, example="Avoid cold water, gentle neck stretch")
    next_follow_up: Optional[str] = Field(None, example="2026-10-20")

class VisitResponse(VisitCreate):
    id: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True