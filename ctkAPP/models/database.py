from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import MODEL

DATABASE_URL = "postgresql://fabio:fabio2002@localhost:5432/CaveDB"

# Configuration de l'engine et de la session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    MODEL.metadata.create_all(engine)

def fermerTout():
    engine.dispose()











