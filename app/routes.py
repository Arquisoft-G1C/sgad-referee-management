from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.database import get_db
from app.model.referee import Referee

router = APIRouter(prefix="/referees", tags=["Referees"])

# Schemas para Swagger
class RefereeCreate(BaseModel):
    user_id: UUID
    license_number: str
    specialties: List[str]
    certification_level: str
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None
    account_holder: Optional[str] = None
    is_available: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "2ff3e5e7-a266-4b62-8401-abf67bade9be",
                "license_number": "ARB-2024-001",
                "specialties": ["futbol", "futsal"],
                "certification_level": "nacional",
                "bank_account": "1234567890",
                "bank_name": "Banco Nacional",
                "account_holder": "Juan Pérez",
                "is_available": True
            }
        }

class RefereeUpdate(BaseModel):
    license_number: Optional[str] = None
    specialties: Optional[List[str]] = None
    certification_level: Optional[str] = None
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None
    account_holder: Optional[str] = None
    is_available: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "is_available": False,
                "bank_account": "9876543210"
            }
        }

# Crear árbitro
@router.post("/", summary="Crear nuevo árbitro")
def create_referee(referee_data: RefereeCreate, db: Session = Depends(get_db)):
    new_referee = Referee(**referee_data.model_dump())
    db.add(new_referee)
    db.commit()
    db.refresh(new_referee)
    return new_referee

# Listar todos los árbitros
@router.get("/", summary="Listar todos los árbitros")
def list_referees(db: Session = Depends(get_db)):
    referees = db.query(Referee).all()
    return referees

# Buscar árbitro por ID
@router.get("/{referee_id}", summary="Buscar árbitro por ID")
def get_referee(referee_id: UUID, db: Session = Depends(get_db)):
    referee = db.query(Referee).filter(Referee.id == referee_id).first()
    if not referee:
        raise HTTPException(status_code=404, detail="Árbitro no encontrado")
    return referee

# Buscar árbitro por user_id
@router.get("/user/{user_id}", summary="Buscar árbitro por user_id")
def get_referee_by_user(user_id: UUID, db: Session = Depends(get_db)):
    referee = db.query(Referee).filter(Referee.user_id == user_id).first()
    if not referee:
        raise HTTPException(status_code=404, detail="Árbitro no encontrado")
    return referee

# Actualizar árbitro
@router.put("/{referee_id}", summary="Actualizar árbitro")
def update_referee(referee_id: UUID, referee_data: RefereeUpdate, db: Session = Depends(get_db)):
    referee = db.query(Referee).filter(Referee.id == referee_id).first()
    if not referee:
        raise HTTPException(status_code=404, detail="Árbitro no encontrado")
    
    update_data = referee_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(referee, key, value)
    
    db.commit()
    db.refresh(referee)
    return referee

# Eliminar árbitro
@router.delete("/{referee_id}", summary="Eliminar árbitro")
def delete_referee(referee_id: UUID, db: Session = Depends(get_db)):
    referee = db.query(Referee).filter(Referee.id == referee_id).first()
    if not referee:
        raise HTTPException(status_code=404, detail="Árbitro no encontrado")
    
    db.delete(referee)
    db.commit()
    return {"message": "Árbitro eliminado correctamente"}