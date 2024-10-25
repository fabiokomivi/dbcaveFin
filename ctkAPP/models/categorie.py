from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import MODEL

class Categorie(MODEL):
    __tablename__= "Categories"
    id = Column(Integer, primary_key=True, nullable=False)
    nom = Column(String, nullable=False)
    description = Column(String, nullable=False)

    boissons = relationship("Boisson", back_populates="categorie", cascade="all, delete-orphan")