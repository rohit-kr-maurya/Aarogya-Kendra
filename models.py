import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    mobile = Column(String, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    city = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")


class Visit(Base):
    __tablename__ = "visits"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    issue = Column(String, nullable=False)
    complaints = Column(Text, nullable=True)
    points = Column(Text, nullable=True)
    advice = Column(Text, nullable=True)
    next_follow_up = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    patient = relationship("Patient", back_populates="visits")