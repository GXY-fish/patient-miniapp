from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.evaluation import Evaluation
from app.models.report import Report
from app.schemas.common import ReportCreate, ReportResponse

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=List[ReportResponse])
def list_reports(
    evaluation_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Report)
    if evaluation_id is not None:
        query = query.filter(Report.evaluation_id == evaluation_id)
    return query.order_by(Report.id.desc()).all()


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("", response_model=ReportResponse)
def create_report(payload: ReportCreate, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.id == payload.evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    report = Report(**payload.model_dump())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
