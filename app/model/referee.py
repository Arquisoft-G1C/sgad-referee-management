import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.database import Base

class Referee(Base):
    __tablename__ = "referees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # Sin ForeignKey

    license_number = Column(String(50), unique=True, nullable=False)
    specialties = Column(ARRAY(String), nullable=False)  # ej. ['futbol', 'futsal']
    certification_level = Column(String(50), nullable=False)  # 'nacional', 'internacional'
    bank_account = Column(String(50), nullable=True)  # Para QR de pagos
    bank_name = Column(String(100), nullable=True)
    account_holder = Column(String(255), nullable=True)
    is_available = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
