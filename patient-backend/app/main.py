from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.session import Base, engine
from app.models import (  # noqa: F401
    DoctorReview,
    Evaluation,
    FollowUpTask,
    Message,
    Patient,
    Report,
)
from app.routers import auth, doctor, evaluations, followups, health, messages, patients, reports, uploads

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = settings.api_v1_prefix
app.include_router(health.router, prefix=api_prefix)
app.include_router(auth.router, prefix=api_prefix)
app.include_router(patients.router, prefix=api_prefix)
app.include_router(evaluations.router, prefix=api_prefix)
app.include_router(reports.router, prefix=api_prefix)
app.include_router(doctor.router, prefix=api_prefix)
app.include_router(messages.router, prefix=api_prefix)
app.include_router(followups.router, prefix=api_prefix)
app.include_router(uploads.router, prefix=api_prefix)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "env": settings.env,
        "docs": "/docs",
        "health": f"{api_prefix}/health",
    }
