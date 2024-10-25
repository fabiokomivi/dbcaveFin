from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import MODEL

class Employe(MODEL):
    __tablename__= "Employes"
    id = Column(Integer, primary_key=True, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    motDePasse = Column(String, nullable=False)
    telephone = Column(String, nullable=False, unique=True)
    addresse = Column(String, nullable=False, unique=True)

    chefId = Column(Integer, ForeignKey('Chefs.id'))
    chef = relationship("Chef", back_populates="employes")

    clients = relationship("Client", back_populates="employe", cascade="all, delete-orphan")

    commandes = relationship("Commande", back_populates="employe", cascade="all, delete-orphan")