from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import MODEL

class Chef(MODEL):
    __tablename__ = "Chefs"
    id = Column(Integer, primary_key=True, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    telephone = Column(String, nullable=False, unique=True)
    addresse = Column(String, nullable=False, unique=True)
    motDePasse = Column(String, nullable=False)

    employes = relationship("Employe", back_populates="chef", cascade="all, delete-orphan")