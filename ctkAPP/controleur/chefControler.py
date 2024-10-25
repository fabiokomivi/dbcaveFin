from models.database import SessionLocal
from models.chef import Chef
import hashlib


def hasher(password):
    passwordBytes = password.encode('utf-8')
    passwordHash = hashlib.sha256(passwordBytes)
    return passwordHash.hexdigest()


def creerChef(nom, prenom, motDePasse , telephone, addresse):
    session = SessionLocal()
    session.add(Chef(nom=nom, prenom=prenom, motDePasse=motDePasse, telephone=telephone, addresse=addresse))
    session.commit()
    session.close()

def obtenirChefPar(id=None, nom=None, motDePasse=None, addresse=None):
    session = SessionLocal()
    chef = session.query(Chef)
    if id:
        chef=chef.filter(Chef.id == id).first()
        session.close()
        return chef
    if nom:
        chef = chef.filter(Chef.nom==nom)
    if motDePasse:
        chef = chef.filter(Chef.motDePasse==hasher(motDePasse))
    if addresse:
        chef = chef.filter(Chef.addresse==addresse)

    session.close()
    return chef.first()


def obtenirChefs():
    session = SessionLocal()
    chefs = session.query(Chef).all()
    session.close()
    return chefs

def modifierChef(chefId=None, addresse=None, password=None):
    session = SessionLocal()
    if addresse:
        chef = session.query(Chef).filter(Chef.addresse==addresse).first()
        if chef:
            if addresse:
                chef.addresse=addresse
            if password:
                chef.motDePasse = hasher(password)
            session.commit()
    session.close()
        



