from models.database import SessionLocal
from sqlalchemy import and_
from models.client import Client
from sqlalchemy.exc import SQLAlchemyError


def creerClient(employeId, nom, prenom, telephone, addresse):
    session = SessionLocal()
    client = Client(employeId=employeId, nom=nom, prenom=prenom, telephone=telephone, addresse=addresse)
    if client:
        session.add(client)
        session.commit()
        session.close()
        return True
    else:
        session.close()
        return False

def obtenirClients():
    session = SessionLocal()
    clients = session.query(Client).all()
    session.close
    return clients

def obtenirClientparAttribue(clientId=None, nom=None, prenom=None, telephone=None, addresse=None, tous=False):
    session = SessionLocal()
    query = session.query(Client)  # Commence par la base de la requête
    
    # Ajoute les filtres uniquement si les valeurs sont spécifiées
    if tous:
        clients = query
    else:
        if nom:
            query = query.filter(Client.nom.ilike(f"%{nom}%"))
        if prenom:
            query = query.filter(Client.prenom.ilike(f"%{prenom}%"))
        if telephone:
            query = query.filter(Client.telephone.ilike(f"%{telephone}%"))
        if addresse:
            query = query.filter(Client.addresse.ilike(f"%{addresse}%"))
        if clientId:
            employe = query.filter(Client.id == clientId).first()
            session.close()
            return employe
    clients = query.all()
    session.close()
    
    return clients

def modifierClient(client_id, nom=None, prenom=None, telephone=None, addresse=None):
    # Ouvrir une session
    session = SessionLocal()
    client = session.query(Client).filter(Client.id == client_id).first()
    if client is None:
        session.close()
        return False
    if nom:
        client.nom = nom
    if prenom:
        client.prenom = prenom
    if telephone:
        client.telephone = telephone
    if addresse:
        client.addresse = addresse
    session.commit()
    return True

def supprimerClient(client_id):
    session = SessionLocal()  # Ouvre une session avec la base de données
    # Rechercher le client par son id
    client = session.query(Client).filter(Client.id == client_id).first()

    if client:
        # Supprimer le client
        session.delete(client)
        session.commit()  # Appliquer les changements dans la base de données
        session.close()  # Fermer la session

def obtenirClientParEmploye(employerId):
    session = SessionLocal()
    clients = session.query(Client).filter(Client.employeId==employerId).all()
    session.close()
    return clients