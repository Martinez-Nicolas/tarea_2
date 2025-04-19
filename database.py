from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Cambiar el nombre de la base de datos
DATABASE_URL = "sqlite:///./vuelos_db.sqlite"  # Aquí cambiamos el nombre de la base de datos

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos con el nuevo nombre
Base.metadata.create_all(bind=engine)

# Función para inyectar sesión en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
