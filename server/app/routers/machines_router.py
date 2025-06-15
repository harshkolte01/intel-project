from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.machine_model import Machine, MachineStatus
from app.database_config import get_db
from datetime import datetime

router = APIRouter(prefix="/machines", tags=["machines"])

@router.get("/")
async def get_machines(db: Session = Depends(get_db)):
    return db.query(Machine).all()

@router.post("/")
async def create_machine(machine: dict, db: Session = Depends(get_db)):
    try:
        # Validate status
        status = machine.get("status", "available")
        if status not in [s.value for s in MachineStatus]:
            raise ValueError(f"Invalid status: {status}")
        
        # Validate priority
        priority = machine.get("priority", 1)
        if not isinstance(priority, int) or priority < 1 or priority > 3:
            raise ValueError(f"Invalid priority: {priority}")

        db_machine = Machine(
            name=machine["name"],
            status=status,
            priority=priority,
            available_from=datetime.now()
        )
        db.add(db_machine)
        db.commit()
        db.refresh(db_machine)
        return db_machine
    except Exception as e:
        print(f"Error creating machine: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to create machine: {str(e)}")