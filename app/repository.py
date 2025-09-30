from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from app import models, schemas
from app.models import Referee
from app.schemas import RefereeCreate, RefereeUpdate


def create_referee(db: Session, referee_in: RefereeCreate) -> Referee:
    db_ref = Referee(**referee_in.dict())
    db.add(db_ref)
    db.commit()
    db.refresh(db_ref)
    return db_ref


def get_referee(db: Session, referee_id: UUID) -> Optional[Referee]:
    return db.query(Referee).filter(Referee.id == referee_id).first()


def get_referee_by_license(db: Session, license_number: str) -> Optional[Referee]:
    return db.query(Referee).filter(Referee.license_number == license_number).first()


def list_referees(db: Session, skip: int = 0, limit: int = 10) -> List[Referee]:
    return db.query(Referee).offset(skip).limit(limit).all()


def update_referee(db: Session, referee_id: UUID, referee_in: RefereeUpdate) -> Optional[Referee]:
    db_ref = db.query(Referee).filter(Referee.id == referee_id).first()
    if not db_ref:
        return None
    update_data = referee_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ref, key, value)
    db.commit()
    db.refresh(db_ref)
    return db_ref


def delete_referee(db: Session, referee_id: UUID) -> bool:
    db_ref = db.query(Referee).filter(Referee.id == referee_id).first()
    if not db_ref:
        return False
    db.delete(db_ref)
    db.commit()
    return True