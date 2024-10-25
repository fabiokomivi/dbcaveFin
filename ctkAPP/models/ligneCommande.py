from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import MODEL

class LigneCommande(MODEL):
    __tablename__ = "LignesCommandes"
    id = Column(Integer, primary_key=True, nullable=False)

    commandeId = Column(Integer, ForeignKey("Commandes.id"), nullable=False)
    boissonId = Column(Integer, ForeignKey("Boissons.id"), nullable=False)
    quantite = Column(Integer, nullable=False)
    prix = Column(Numeric, nullable=False)
    prixTotal = Column(Numeric, nullable=False)

    commande = relationship("Commande", back_populates="lignesCommande")
    boisson = relationship("Boisson", back_populates="lignesCommande")
    