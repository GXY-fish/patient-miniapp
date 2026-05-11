from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import engine

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    return {"status": "ok", "service": "stoma-ai-backend"}


@router.get("/db")
def health_check_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
