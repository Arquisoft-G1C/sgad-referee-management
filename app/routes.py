from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app import repository, schemas

router = APIRouter(prefix="/referees", tags=["Referees"])


@router.post("/", response_model=RefereeOut)
def create_referee(referee: RefereeCreate, db: Session = Depends(get_db)):
    db_ref = referee_repository.get_referee_by_license(db, referee.license_number)
    if db_ref:
        raise HTTPException(status_code=400, detail="License number already registered")
    return referee_repository.create_referee(db, referee)


@router.get("/{referee_id}", response_model=RefereeOut)
def get_referee(referee_id: UUID, db: Session = Depends(get_db)):
    db_ref = referee_repository.get_referee(db, referee_id)
    if not db_ref:
        raise HTTPException(status_code=404, detail="Referee not found")
    return db_ref


@router.get("/", response_model=List[RefereeOut])
def list_referees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return referee_repository.list_referees(db, skip=skip, limit=limit)


@router.put("/{referee_id}", response_model=RefereeOut)
def update_referee(referee_id: UUID, referee: RefereeUpdate, db: Session = Depends(get_db)):
    db_ref = referee_repository.update_referee(db, referee_id, referee)
    if not db_ref:
        raise HTTPException(status_code=404, detail="Referee not found")
    return db_ref


@router.delete("/{referee_id}", response_model=dict)
def delete_referee(referee_id: UUID, db: Session = Depends(get_db)):
    success = referee_repository.delete_referee(db, referee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Referee not found")
    return {"detail": "Referee deleted successfully"}