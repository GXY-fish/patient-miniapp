from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.patient import Patient
from app.schemas.common import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("", response_model=List[PatientResponse])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).order_by(Patient.id.desc()).all()


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("", response_model=PatientResponse)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    medical_no = payload.medical_no.strip() if payload.medical_no else None
    if medical_no == "":
        medical_no = None

    existing_by_phone = db.query(Patient).filter(Patient.phone == payload.phone).first()
    existing_by_medical_no = (
        db.query(Patient)
        .filter(Patient.medical_no == medical_no)
        .first()
        if medical_no
        else None
    )

    target = existing_by_phone or existing_by_medical_no

    if target and existing_by_phone and existing_by_medical_no and existing_by_phone.id != existing_by_medical_no.id:
        raise HTTPException(status_code=400, detail="Phone and medical number belong to different patients")

    if target:
        if existing_by_phone and medical_no:
            conflicting_medical_no = (
                db.query(Patient)
                .filter(Patient.medical_no == medical_no, Patient.id != target.id)
                .first()
            )
            if conflicting_medical_no:
                conflicting_medical_no.medical_no = None
        target.name = payload.name
        target.phone = payload.phone
        target.medical_no = medical_no
        target.stoma_type = payload.stoma_type
        target.surgery_date = payload.surgery_date
        target.privacy_authorized = payload.privacy_authorized
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Phone or medical number already exists")
        db.refresh(target)
        return target

    patient = Patient(**payload.model_dump(exclude={"medical_no"}), medical_no=medical_no)
    db.add(patient)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Phone or medical number already exists")
    db.refresh(patient)
    return patient
