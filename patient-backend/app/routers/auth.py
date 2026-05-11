from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    phone: str
    code: str | None = None
    role: str = "patient"


@router.post("/login")
def login(payload: LoginRequest):
    if payload.role not in {"patient", "doctor"}:
        raise HTTPException(status_code=400, detail="Invalid role")
    return {
        "access_token": f"demo-access-token:{payload.phone}:{payload.role}",
        "token_type": "bearer",
        "phone": payload.phone,
        "role": payload.role,
    }


@router.get("/profile")
def profile(role: str = "patient"):
    return {
        "id": 1,
        "name": "示例用户",
        "role": role,
    }
