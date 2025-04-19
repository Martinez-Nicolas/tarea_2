from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modelo de SQLAlchemy para la base de datos
class Vuelo(Base):
    __tablename__ = 'vuelos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    tipo = Column(String)
    prioridad = Column(Integer)

# Modelo Pydantic para validaciones de entrada
class VueloBase(BaseModel):
    nombre: str
    tipo: str
    prioridad: int

    class Config:
        # Actualiza de 'orm_mode' a 'from_attributes' para Pydantic v2
        from_attributes = True
