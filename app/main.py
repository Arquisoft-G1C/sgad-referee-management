from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import router as referee_router

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Referee Service")

# Incluir rutas
app.include_router(referee_router)
