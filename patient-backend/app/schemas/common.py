from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(ORMBaseModel):
    id: int
    title: str
    content: str
    time: str
    unread: bool


class DashboardResponse(ORMBaseModel):
    pending_total: int
    high_risk_total: int
    timeout_total: int
    done_today: int


class PatientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    phone: str = Field(min_length=6, max_length=20)
    medical_no: Optional[str] = Field(default=None, max_length=50)
    stoma_type: str = Field(min_length=1, max_length=30)
    surgery_date: date
    privacy_authorized: bool = False


class PatientResponse(PatientCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EvaluationCreate(BaseModel):
    patient_id: int
    photos: List[str] = Field(default_factory=list)
    symptoms: Dict[str, Any] = Field(default_factory=dict)


class EvaluationResponse(EvaluationCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    risk_level: Optional[str] = None
    ai_summary: Optional[str] = None
    doctor_summary: Optional[str] = None
    created_at: Optional[datetime] = None


class ReviewCreate(BaseModel):
    final_risk_level: str
    complication_tags: List[str] = Field(default_factory=list)
    revision_flag: bool = False
    revision_reason: Optional[str] = None
    care_advice: str
    disposition: str
    urgent_level: Optional[str] = None
    followup_days: int = 7


class ReportCreate(BaseModel):
    evaluation_id: int
    final_conclusion: str
    care_advice: str
    disposition: str


class ReportResponse(ORMBaseModel):
    id: int
    evaluation_id: int
    final_conclusion: str
    care_advice: str
    disposition: str
    created_at: Optional[datetime] = None


class UploadResponse(BaseModel):
    filename: str
    path: str
    size: int
