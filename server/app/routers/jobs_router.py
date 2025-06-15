from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.job_model import Job
from app.database_config import get_db

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/")
async def create_job(job: dict, db: Session = Depends(get_db)):
    db_job = Job(job_id=job["job_id"], operations=job["operations"])
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/")
async def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()