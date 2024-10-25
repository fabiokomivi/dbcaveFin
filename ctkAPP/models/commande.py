from sqlalchemy import Enum, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import MODEL
from datetime import datetime, timezone

class Commande(MODEL):
    __tablename__ = "Commandes"
    id = Column(Integer, primary_key=True, nullable=False)

    clientId = Column(Integer, ForeignKey("Clients.id"))
    client = relationship("Client", back_populates="commandes")
    dateCommande = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    employeId = Column(Integer, ForeignKey("Employes.id"))
    employe = relationship("Employe", back_populates="commandes")
    etat = Column(Enum('validée', 'en attente', name='etat_commande'), nullable=False, default='en attente')

    lignesCommande = relationship("LigneCommande", back_populates="commande", cascade="all, delete-orphan")

    def prixTotal(self):
        return sum(ligne.prixTotal for ligne in self.lignesCommande)
    
    def avoirJourMoisAnnee(self):
        return self.dateCommande.day, self.dateCommande.month, self.dateCommande.year
        