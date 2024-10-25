from models.database import SessionLocal
from models.categorie import Categorie
from sqlalchemy.orm import joinedload


def creerCategorie(nom, description):
    session = SessionLocal()
    session.add(Categorie(nom=nom, description=description))
    session.commit()
    session.close()
    return True


def obtenirCategorieParAttribue(categorieId="", nom="", description="", tous=False):
    session = SessionLocal()
    query = session.query(Categorie).options(joinedload(Categorie.boissons))
    if tous:
        session.close()
        return query.all()
    else:
        if categorieId:
            query = query.filter(Categorie.id == categorieId)
        if nom:
            query = query.filter(Categorie.nom.ilike(f"%{nom}%"))
        if description:
            query = query.filter(Categorie.description.ilike(f"%{description}%"))
        session.close()
        return query.all()

def modifierCategorie(categorieId, nom, description):
    session = SessionLocal()
    categorie = session.query(Categorie).filter(Categorie.id==categorieId).first()
    if nom:
        categorie.nom = nom
    if description:
        categorie.description = description
    session.commit()
    session.close()
    return True

def supprimerCategorie(categorieId):
    session = SessionLocal()
    categorie = session.query(Categorie).filter(Categorie.id==categorieId).first()
    if categorie is None:
        session.close()
        return False
    else:
        session.delete(categorie)
        session.commit()
        session.close()
        return True