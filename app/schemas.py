from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class RefereeBase(BaseModel):
    license_number: str
    specialties: List[str]
    certification_level: str
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None
    account_holder: Optional[str] = None
    is_available: bool = True

class RefereeCreate(RefereeBase):
    user_id: UUID

class RefereeUpdate(BaseModel):
    specialties: Optional[List[str]] = None
    certification_level: Optional[str] = None
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None
    account_holder: Optional[str] = None
    is_available: Optional[bool] = None

class RefereeInDB(RefereeBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True