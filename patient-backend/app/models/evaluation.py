from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.sql import func

from app.db.session import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    status = Column(String(40), nullable=False, default="draft")
    risk_level = Column(String(20), nullable=True)
    photos = Column(JSON, nullable=False, default=list)
    symptoms = Column(JSON, nullable=False, default=dict)
    ai_summary = Column(Text, nullable=True)
    doctor_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
