from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.genetic_algo import generate_schedule
from app.database_config import get_db
from app.models.job_model import Job
from app.models.machine_model import Machine

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.get("/", response_model=list)
async def get_schedule(db: Session = Depends(get_db)):
    try:
        jobs = db.query(Job).all()
        machines = db.query(Machine).all()
        schedule = generate_schedule(jobs, machines)
        return schedule
    except Exception as e:
        print(f"Error generating schedule: {e}")
        return []