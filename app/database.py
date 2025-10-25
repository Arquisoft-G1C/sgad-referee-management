import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ==========================
# 1️⃣ Cargar variables del .env
# ==========================
load_dotenv()

# ==========================
# 2️⃣ Configuración centralizada
# ==========================
class Settings:
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "sgad_db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "admin123")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "admin123")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    # Construir la URL de conexión dinámica si no está definida
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

settings = Settings()

# ==========================
# 3️⃣ Conexión SQLAlchemy
# ==========================
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,      # Cambia a False en producción
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ==========================
# 4️⃣ Función auxiliar para dependencias (FastAPI)
# ==========================
def get_db():
    """
    Dependencia para inyectar sesiones de base de datos en los endpoints de FastAPI.
    Ejemplo:
        def read_items(db: Session = Depends(get_db)):
            return db.query(Model).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
