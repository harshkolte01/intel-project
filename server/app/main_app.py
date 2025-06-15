from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import datetime
from app.routers import jobs_router, machines_router, schedule_router
from app.database_config import engine, get_db
from app.models.job_model import Job
from app.models.machine_model import Machine, MachineStatus

app = FastAPI(title="Smart Scheduling System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables explicitly
def create_tables():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS machines (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                status VARCHAR DEFAULT 'available',
                priority INTEGER DEFAULT 1,
                available_from TIMESTAMP
            );
        """))
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                job_id VARCHAR UNIQUE NOT NULL,
                operations JSONB NOT NULL
            );
        """))
        connection.commit()

create_tables()
Job.metadata.create_all(bind=engine)
Machine.metadata.create_all(bind=engine)

app.include_router(jobs_router.router)
app.include_router(machines_router.router)
app.include_router(schedule_router.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    db: Session = next(get_db())
    try:
        # Check if machines exist
        if not db.query(Machine).first():
            machines = [
                Machine(
                    name="Machine1",
                    status=MachineStatus.AVAILABLE,
                    priority=1,
                    available_from=datetime.now()
                ),
                Machine(
                    name="Machine2",
                    status=MachineStatus.MAINTENANCE,
                    priority=2,
                    available_from=datetime.now()
                )
            ]
            db.add_all(machines)
            db.commit()
            for machine in machines:
                db.refresh(machine)
            print("Added 2 sample machines")

        # Check if jobs exist
        if not db.query(Job).first():
            jobs = [
                Job(
                    job_id="JOB001",
                    operations=[
                        {"machine_id": "1", "duration": "30"},
                        {"machine_id": "2", "duration": "20"}
                    ]
                ),
                Job(
                    job_id="JOB002",
                    operations=[
                        {"machine_id": "2", "duration": "15"},
                        {"machine_id": "1", "duration": "25"}
                    ]
                ),
                Job(
                    job_id="JOB003",
                    operations=[
                        {"machine_id": "1", "duration": "10"}
                    ]
                )
            ]
            db.add_all(jobs)
            db.commit()
            for job in jobs:
                db.refresh(job)
            print("Added 3 sample jobs")
    except Exception as e:
        print(f"Error in startup_event: {e}")
    finally:
        db.close()