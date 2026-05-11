# Stoma AI Backend Skeleton

A minimal FastAPI backend for the stoma assessment system.

## Features
- FastAPI application bootstrap
- Versioned API routing
- Health endpoint
- Placeholder auth, patient, evaluation, report, doctor, message, and follow-up endpoints
- PostgreSQL, Redis, and Docker Compose scaffolding

## Local run
1. Copy `.env.example` to `.env`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `uvicorn app.main:app --reload`

## Docker run
```bash
docker compose up --build
```

## API base
- Local: `http://127.0.0.1:8000/api/v1`
- Docs: `http://127.0.0.1:8000/docs`
