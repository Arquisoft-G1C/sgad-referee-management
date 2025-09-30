from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app import schemas, models, repository

# ==============
# CRUD con reglas de negocio
# ==============

def create_referee_service(db: Session, referee_in: RefereeCreate) -> Referee:
    # Regla: licencia única
    existing = referee_repository.get_referee_by_license(db, referee_in.license_number)
    if existing:
        raise ValueError("License number already registered")
    return referee_repository.create_referee(db, referee_in)


def get_referee_service(db: Session, referee_id: UUID) -> Optional[Referee]:
    return referee_repository.get_referee(db, referee_id)


def list_referees_service(db: Session, skip: int = 0, limit: int = 10) -> List[Referee]:
    return referee_repository.list_referees(db, skip, limit)


def update_referee_service(db: Session, referee_id: UUID, referee_in: RefereeUpdate) -> Optional[Referee]:
    return referee_repository.update_referee(db, referee_id, referee_in)


def delete_referee_service(db: Session, referee_id: UUID) -> bool:
    return referee_repository.delete_referee(db, referee_id)


# ==============
# Reglas de negocio específicas
# ==============

def assign_referee_to_match(db: Session, referee_id: UUID, match_id: UUID):
    """
    Reglas:
    1. Un árbitro solo puede estar en un partido a la vez.
    2. Un árbitro no puede arbitrar un partido si uno de los dos equipos también estuvo en su último partido arbitrado.
    """

    referee = referee_repository.get_referee(db, referee_id)
    if not referee:
        raise ValueError("Referee not found")

    match = match_repository.get_match(db, match_id)
    if not match:
        raise ValueError("Match not found")

    # Regla 1: ¿ya tiene un partido en curso?
    current_match = referee_assignment_repository.get_active_match_for_referee(db, referee_id)
    if current_match:
        raise ValueError(f"Referee is already assigned to match {current_match.id}")

    # Regla 2: equipos del último partido
    last_match = referee_assignment_repository.get_last_match_for_referee(db, referee_id)
    if last_match:
        if (match.team_a in [last_match.team_a, last_match.team_b]) or \
           (match.team_b in [last_match.team_a, last_match.team_b]):
            raise ValueError("Referee cannot arbitrate consecutive matches with the same team")

    # Si pasa las reglas → asignar
    return referee_assignment_repository.create_assignment(db, referee_id, match_id)
