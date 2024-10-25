from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import MODEL

class Stock(MODEL):
    __tablename__ = "Stocks"
    id = Column(Integer, primary_key=True)
    quantite = Column(Integer, nullable=False)

    boissonId = Column(Integer, ForeignKey("Boissons.id"))

    boisson = relationship("Boisson", back_populates="stock")
