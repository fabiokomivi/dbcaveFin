from models.database import SessionLocal
from sqlalchemy.orm import joinedload
from models.employe import Employe
from models.commande import Commande
from sqlalchemy.orm import joinedload
import hashlib

def hasher(password):
    passwordBytes = password.encode('utf-8')
    passwordHash = hashlib.sha256(passwordBytes)
    return passwordHash.hexdigest()


def creerEmploye(chefId, nom, prenom, telephone, addresse, motDePasse ):
    session = SessionLocal()
    session.add(Employe(chefId = chefId, nom=nom, prenom=prenom, motDePasse=hasher(motDePasse), telephone=telephone, addresse=addresse))
    session.commit()
    session.close()

def obtenirEmployePar(id=None, nom=None, prenom=None, telephone=None, addresse=None, mdp=None, connexion=False):
    session = SessionLocal()
    try:
        employes = session.query(Employe)
        if id:
            employes = employes.filter(Employe.id==id).first()
        else:
            if telephone:
                employes = employes.filter(Employe.telephone.ilike(f"%{telephone}%"))
            
            if addresse:
                employes = employes.filter(Employe.addresse.ilike(f"%{addresse}%"))
            if nom:
                employes = employes.filter(Employe.nom==nom) if connexion else\
                    employes.filter(Employe.nom.ilike(f"%{nom}%"))
            if prenom:
                employes = employes.filter(Employe.prenom==prenom) if connexion else\
                    employes.filter(Employe.prenom.ilike(f"%{prenom}%"))
            if mdp:
                employes = employes.filter(Employe.motDePasse==hasher(mdp))
            
            employes = employes.all()
    finally:
        session.close()
        return employes
        


def obtenirEmploye():
    session = SessionLocal()
    employes = (
        session.query(Employe)
        .options(
            joinedload(Employe.commandes)
            .joinedload(Commande.lignesCommande)  # Remplace 'lignecommande' par le nom correct de la relation
        )
        .all()
    )
    session.close()
    return employes


def modifierEmploye(employeId, nom=None, prenom=None, telephone=None, addresse=None, mdp=None):
    # Ouvrir une session
    session = SessionLocal()
    employe = session.query(Employe).filter(Employe.id == employeId).first()
    if employe is None:
        session.close()
        return False
    if nom:
        employe.nom = nom
    if prenom:
        employe.prenom = prenom
    if telephone:
        employe.telephone = telephone
    if addresse:
        employe.addresse = addresse
    if mdp:
        employe.motDePasse = hasher(mdp)
    session.commit()
    session.close()
    return True

def supprimerEmploye(employeId):
    session = SessionLocal()
    employe = session.query(Employe).filter(Employe.id==employeId).first()
    if employe:
        session.delete(employe)
        session.commit()
        session.close()
        return True
    else:
        session.close()
        return False
