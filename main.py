# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./candidato.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir el modelo de datos de candidato
class Candidato(Base):
    __tablename__ = "candidatos"

    dni = Column(String, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Definir el esquema de datos para validar la entrada del usuario
class CandidatoIn(BaseModel):
    dni: str
    nombre: str
    apellido: str

# Definir el endpoint para manejar la solicitud POST de candidatos
@app.post("/candidato/")
async def create_candidato(candidato: CandidatoIn):
    # Crear una sesión de base de datos
    db = SessionLocal()
    # Crear una instancia del modelo Candidato con los datos recibidos
    db_candidato = Candidato(**candidato.dict())
    # Agregar el candidato a la base de datos
    db.add(db_candidato)
    db.commit()
    db.refresh(db_candidato)
    return {"message": "Candidato creado correctamente"}
