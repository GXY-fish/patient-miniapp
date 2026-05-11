from fastapi import APIRouter

router = APIRouter(prefix="/followups", tags=["followups"])

FOLLOWUPS = [
    {
        "id": 1,
        "patient_id": 1,
        "evaluation_id": 1,
        "status": "pending",
        "due_date": "2026-04-27",
    }
]


@router.get("")
def list_followups():
    return FOLLOWUPS
