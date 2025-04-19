from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modelo SQLAlchemy
class Vuelo(Base):
    __tablename__ = 'vuelos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    tipo = Column(String)
    prioridad = Column(Integer)

# Modelo Pydantic
class VueloBase(BaseModel):
    nombre: str
    tipo: str
    prioridad: int

    class Config:
        from_attributes = True  # Pydantic v2 compatible
