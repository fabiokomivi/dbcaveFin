from datetime import datetime, timezone


class CommandeTmp:
    def __init__(self, id=None, clientId=None, employeId=None, date=None, connue=True) -> None:
        self.id = id
        self.clientId = clientId
        self.employeId = employeId

        self.lignesConnues = []
        self.lignesInconnues = []

        self.lignesConnuesSupprimes = []
        self.lignesInconnuesSupprimes = []

        self.etat = "en attente"
        self.date = date if connue else datetime.now(timezone.utc)
        self.connue = connue
        self.finalise = False

        self.idConnues=[]
        self.idInconnues=[]

        self.idConnuesSupprimes=[]
        self.idInconnuesSupprimes=[]

        self.ligneCourrante = None

        self.valide = False

    def valider(self):
        self.valide = True

    def ajouteLigneInconnue(self, lgncmd):
        if lgncmd.id is None:
            lgncmd.id = f"new_{len(self.lignesInconnues)}"
        self.lignesInconnues.append(lgncmd)
        self.idInconnues.append(lgncmd.id)


    def ajouteLigneConnue(self, lgncmd):
        self.lignesConnues.append(lgncmd)
        self.idConnues.append(f"{lgncmd.id}")

    def marquerEnAttente(self):
        self.etat = "en attente"

    def estConnue(self):
        return self.connue
    
    def finaliser(self):
        self.finalise = True

    def supprimerLigne(self, ligne):
        if ligne.estConnue():
            self.lignesConnuesSupprimes.append(ligne)
            self.idConnuesSupprimes.append(str(ligne.id))
            self.lignesConnues.remove(ligne)
            self.idConnuesSupprimes.remove(str(ligne.id))
        else:
            self.lignesInconnuesSupprimes.append(ligne)
            self.idInconnuesSupprimes.append(str(ligne.id))

class LigneCommandeTmp:
    def __init__(self, id=None, boissonId=None, prix=None, quantite=None, connue=True):
        self.id = id
        self.boissonId = boissonId
        self.quantite = quantite
        self.prix=prix
        self.connue = connue
        self.modifie = False

    def estConnue(self):
        return self.connue
