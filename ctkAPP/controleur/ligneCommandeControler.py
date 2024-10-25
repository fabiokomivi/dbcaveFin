from models.database import SessionLocal
from models.ligneCommande import LigneCommande
from sqlalchemy.exc import SQLAlchemyError

def AjouterLigneCommande(commandeId, boissonId, quantite, prix, prixTotal):
    session = SessionLocal()
    nouvelleLigneCommande = LigneCommande(commandeId=commandeId, boissonId=boissonId, quantite=quantite, prix=prix, prixTotal=prixTotal)
    session.add(nouvelleLigneCommande)
    session.commit()



def obtenirLigneCommandeParId(ligneCommandeId):
    session = SessionLocal()
    ligneCommande = session.query(LigneCommande).filter(LigneCommande.id==ligneCommandeId).first()
    session.close()
    return ligneCommande


def ModifierLigneCommande(ligneCommandeId, nouvelleQuantite=None):
    ans = False
    session = SessionLocal()
    ligneCommande = session.query(LigneCommande).filter(LigneCommande.id==ligneCommandeId).first()
    if ligneCommande:
        ligneCommande.quantite = nouvelleQuantite
        ligneCommande.prixTotal = ligneCommande.prix*nouvelleQuantite
        session.commit()
        ans = True
    session.close()
    return ans



def SupprimerLigneCommande(ligneCommandeId):
    session = SessionLocal()
    ligneCommande = session.query(LigneCommande).filter(LigneCommande.id==ligneCommandeId).first()
    if ligneCommande:
        session.delete(ligneCommande)
        session.commit()


def obtenirLigneDeCommandes(commandeId):
    session = SessionLocal()
    lignesCommande = session.query(LigneCommande).filter_by(commandeId=commandeId).all()
    return lignesCommande

