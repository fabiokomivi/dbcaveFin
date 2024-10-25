from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Déclaration de la base
Base = declarative_base()

# Modèle Chef
class Chef(Base):
    __tablename__ = 'chefs'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    employes = relationship("Employe", back_populates="chef")

# Modèle Employé
class Employe(Base):
    __tablename__ = 'employes'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    chef_id = Column(Integer, ForeignKey('chefs.id'))
    chef = relationship("Chef", back_populates="employes")
    commandes = relationship("Commande", back_populates="employe")

# Modèle Client
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    commandes = relationship("Commande", back_populates="client")

# Modèle Catégorie de Boissons
class CategorieBoisson(Base):
    __tablename__ = 'categories_boissons'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    boissons = relationship("Boisson", back_populates="categorie")

# Modèle Boisson
class Boisson(Base):
    __tablename__ = 'boissons'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    categorie_id = Column(Integer, ForeignKey('categories_boissons.id'))
    categorie = relationship("CategorieBoisson", back_populates="boissons")
    stock = relationship("Stock", uselist=False, back_populates="boisson")

# Modèle Commande
class Commande(Base):
    __tablename__ = 'commandes'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    employe_id = Column(Integer, ForeignKey('employes.id'))
    client = relationship("Client", back_populates="commandes")
    employe = relationship("Employe", back_populates="commandes")

# Modèle Stock
class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    boisson_id = Column(Integer, ForeignKey('boissons.id'))
    quantite = Column(Integer, nullable=False)
    boisson = relationship("Boisson", back_populates="stock")

# Configuration de la base de données (SQLite ici, mais tu peux utiliser PostgreSQL ou autre)
engine = create_engine('sqlite:///gestion_cave.db', echo=True)

# Créer les tables dans la base de données
Base.metadata.create_all(engine)

# Création d'une session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session()

# Exemple d'ajout de données
def ajouter_donnees():
    chef1 = Chef(nom="Chef 1")
    client1 = Client(nom="Client 1")
    categorie1 = CategorieBoisson(nom="Vin")
    boisson1 = Boisson(nom="Bordeaux", categorie=categorie1)
    employe1 = Employe(nom="Employé 1", chef=chef1)
    stock1 = Stock(boisson=boisson1, quantite=100)
    commande1 = Commande(client=client1, employe=employe1)

    # Ajouter les objets à la session
    session.add(chef1)
    session.add(client1)
    session.add(categorie1)
    session.add(boisson1)
    session.add(employe1)
    session.add(stock1)
    session.add(commande1)

    # Commit pour enregistrer les modifications
    session.commit()

# Exécuter la fonction pour ajouter des données
ajouter_donnees()
