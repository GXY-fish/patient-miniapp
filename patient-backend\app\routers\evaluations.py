from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.evaluation import Evaluation
from app.models.patient import Patient
from app.schemas.common import EvaluationCreate, EvaluationResponse

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.get("", response_model=List[EvaluationResponse])
def list_evaluations(
    patient_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Evaluation)
    if patient_id is not None:
        query = query.filter(Evaluation.patient_id == patient_id)
    return query.order_by(Evaluation.id.desc()).all()


@router.get("/{evaluation_id}", response_model=EvaluationResponse)
def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation


@router.post("", response_model=EvaluationResponse)
def create_evaluation(payload: EvaluationCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    evaluation = Evaluation(
        patient_id=payload.patient_id,
        photos=payload.photos,
        symptoms=payload.symptoms,
        status="pending_doctor_review",
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation
