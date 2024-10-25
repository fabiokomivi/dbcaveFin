from sqlalchemy import  Column, String, Integer, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from .base import MODEL


class Boisson(MODEL):
    __tablename__= "Boissons"
    id = Column(Integer, primary_key=True, nullable=False)
    nom = Column(String, nullable=False)
    prix = Column(Integer, nullable=False)
    image = Column(LargeBinary, nullable=True)

    categorieId = Column(Integer, ForeignKey("Categories.id"))
    categorie = relationship("Categorie", back_populates="boissons")

    stock = relationship("Stock", back_populates="boisson", uselist=False, cascade="all, delete-orphan")

    lignesCommande = relationship("LigneCommande", back_populates="boisson")