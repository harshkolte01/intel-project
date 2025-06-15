from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.database_config import Base
import enum

class MachineStatus(str, enum.Enum):
    AVAILABLE = "available"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(Enum(MachineStatus), default=MachineStatus.AVAILABLE)
    priority = Column(Integer, default=1)  # 1 (high), 2 (medium), 3 (low)
    available_from = Column(DateTime)