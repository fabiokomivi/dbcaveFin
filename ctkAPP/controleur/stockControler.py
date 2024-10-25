from models.database import SessionLocal
from models.stock import Stock




def obtenirStock():
    session = SessionLocal()
    stocks = session.query(Stock).all()
    session.close()
    return stocks


def obtenirStockPar(stockId="", quantite=""):
    session = SessionLocal()
    stocks = session.query(Stock)
    if stockId:
        stock = stocks.filter(Stock.id==stockId).first()
    if quantite:
        stock = stocks.filter(Stock.quantite<=quantite).all()

    session.close()
    return stock

def ajouterStock(stockId, quantite=0):
    session = SessionLocal()
    stock = session.query(Stock).filter(Stock.id==stockId).first()
    if stock:
        stock.quantite+=quantite
        session.commit()
    session.close()
    return True

def obtenirStockParBoisson(boissonId):
    session = SessionLocal()
    stock = session.query(Stock).filter(Stock.boissonId==boissonId).first()
    session.close()
    return stock

