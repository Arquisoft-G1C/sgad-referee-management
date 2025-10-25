from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router as referee_router
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI(title="Referee Service")

# Cors para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(referee_router)

@app.get("/")
def root():
    return {"message": "Referee Management Service", "status": "active"}