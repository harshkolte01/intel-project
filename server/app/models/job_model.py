from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.database_config import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    operations = Column(JSON)  # List of {machine_id, duration}
    