from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import require_role
from app.models.doctor_review import DoctorReview
from app.models.evaluation import Evaluation
from app.models.patient import Patient
from app.models.report import Report
from app.schemas.common import ReviewCreate

router = APIRouter(prefix="/doctor", tags=["doctor"])


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("doctor")),
):
    pending_total = db.query(Evaluation).filter(Evaluation.status == "pending_doctor_review").count()
    high_risk_total = db.query(Evaluation).filter(Evaluation.risk_level == "高").count()
    return {
        "pending_total": pending_total,
        "high_risk_total": high_risk_total,
        "timeout_total": 0,
        "done_today": db.query(Evaluation).filter(Evaluation.status == "completed").count(),
    }


@router.get("/cases")
def list_cases(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("doctor")),
):
    cases = (
        db.query(Evaluation, Patient)
        .join(Patient, Evaluation.patient_id == Patient.id)
        .order_by(Evaluation.id.desc())
        .all()
    )
    result = []
    today = date.today()
    for evaluation, patient in cases:
        masked_name = f"{patient.name[0]}*" if patient.name else "*"
        postop_days = (today - patient.surgery_date).days if patient.surgery_date else 0
        result.append(
            {
                "case_id": evaluation.id,
                "patient_name_masked": masked_name,
                "postop_days": max(postop_days, 0),
                "ai_risk_level": evaluation.risk_level or "未评估",
                "queue_priority": "P1" if evaluation.risk_level == "高" else "P2",
                "case_status": evaluation.status,
            }
        )
    return result


@router.get("/cases/{case_id}")
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("doctor")),
):
    item = (
        db.query(Evaluation, Patient)
        .join(Patient, Evaluation.patient_id == Patient.id)
        .filter(Evaluation.id == case_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Case not found")
    evaluation, patient = item
    return {
        "case_id": evaluation.id,
        "patient_name_masked": f"{patient.name[0]}*" if patient.name else "*",
        "photos": evaluation.photos,
        "ai_summary": evaluation.ai_summary,
        "ai_confidence": 0.86,
        "case_status": evaluation.status,
    }


@router.post("/cases/{case_id}/review")
def review_case(
    case_id: int,
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("doctor")),
):
    evaluation = db.query(Evaluation).filter(Evaluation.id == case_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Case not found")

    evaluation.risk_level = payload.final_risk_level
    evaluation.doctor_summary = payload.care_advice
    evaluation.status = "completed"

    review = DoctorReview(
        evaluation_id=case_id,
        doctor_name="系统医生",
        revision_reason=payload.revision_reason,
        urgent_level=payload.urgent_level,
    )
    report = Report(
        evaluation_id=case_id,
        final_conclusion=f"风险等级：{payload.final_risk_level}；并发症标签：{','.join(payload.complication_tags) or '无'}",
        care_advice=payload.care_advice,
        disposition=payload.disposition,
    )
    db.add(review)
    db.add(report)
    db.commit()
    db.refresh(report)

    return {"message": "review saved", "report_id": report.id}
