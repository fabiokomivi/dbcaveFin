from datetime import datetime



class logs:
    def __init__(self) -> None:
        self.clientLogs = open("ctkAPP/pages/journalisation/logs/clientLogs.txt", '+a')
        self.employeLogs = open("ctkAPP/pages/journalisation/logs/employeLogs.txt", '+a')
        self.connexionLogs = open("ctkAPP/pages/journalisation/logs/connexionLogs.txt", '+a')
        self.commandeLogs = open("ctkAPP/pages/journalisation/logs/commandeLogs.txt", '+a')
        self.categorieLogs = open("ctkAPP/pages/journalisation/logs/categorieLogs.txt", '+a')
        self.boissonLogs = open("ctkAPP/pages/journalisation/logs/boissonLogs.txt", '+a')
        self.stockLogs = open("ctkAPP/pages/journalisation/logs/stockLogs.txt", '+a')

    def logClient(self, client, utilisateur, clientB=None, mode=1):
        if mode==1:
            self.clientLogs.write(f"creation du client: ({client.nom} {client.prenom} {client.telephone})\
 le {datetime.now().strftime('%d/%m/%Y %H:%M')} par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode==2:
            self.clientLogs.write(f"modification du client: ({client.nom} {client.prenom} {client.telephone}) \
-> ({clientB.nom} {clientB.prenom} {clientB.telephone}) le {datetime.now().strftime('%d/%m/%Y %H:%M')} par \
({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        self.fermeture()
            
    def logEmploye(self, employe, utilisateur, employeB=None, mode=1):
        if mode==1:
            self.employeLogs.write(f"creation de l'employe: ({employe.nom} {employe.prenom} {employe.telephone}) le \
{datetime.now().strftime('%d/%m/%Y %H:%M')} par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode==2:
            self.employeLogs.write(f"modification de l'employe: ({employe.nom} {employe.prenom} {employe.telephone}) \
-> ({employeB.nom} {employeB.prenom} {employeB.telephone}) le {datetime.now().strftime('%d/%m/%Y %H:%M')} par \
                                    ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode == 3:
            self.employeLogs.write(f"suppression de l'employe: ({employe.nom} {employe.prenom} {employe.telephone}) le \
{datetime.now().strftime('%d/%m/%Y %H:%M')} par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        self.fermeture()
            
    def logBoisson(self, boisson, utilisateur, boissonB=None, mode=1):
        if mode==1:
            self.boissonLogs.write(f"creation de la boisson: ({boisson.nom} {boisson.prix} {boisson.categorie.nom}) le \
{datetime.now().strftime('%d/%m/%Y %H:%M')} par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode==2:
            self.boissonLogs.write(f"modification de la boisson: ({boisson.nom} {boisson.prix} {boisson.categorie.nom}) \
-> ({boissonB.nom} {boissonB.prix} {boissonB.categorie.nom}) le {datetime.now().strftime('%d/%m/%Y %H:%M')} par \
({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode == 3:
            self.boissonLogs.write(f"suppression de la boisson: ({boisson.nom} {boisson.prix} {boisson.categorie.nom}) le \
{datetime.now().strftime('%d/%m/%Y %H:%M')} par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        self.fermeture()
            
    def logCategorie(self, categorie, utilisateur, categorieB=None, mode=1):
        if mode==1:
            self.categorieLogs.write(f"creation de la categorie: ({categorie.nom}) le \
{datetime.now().strftime('%d/%m/%Y %H:%M')} par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode==2:
            self.categorieLogs.write(f"modification de la categorie: ({categorie.nom}) \
-> ({categorieB.nom}) le {datetime.now().strftime('%d/%m/%Y %H:%M')} par \
({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode == 3:
            self.categorieLogs.write(f"suppression de la categorie: ({categorie.nom}) le \
{datetime.now().strftime('%d/%m/%Y %H:%M')} par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        self.fermeture()
            
            
    def logConnexion(self, utilisateur, mode=1):
        if mode==1:
            self.connexionLogs.write(f"connexion de ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone}) le {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        elif mode==2:
            self.connexionLogs.write(f"deconnexion de ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone}) le {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        self.fermeture()

    def logCommande(self, commande, utilisateur, mode=1):
        if mode==1:
            self.commandeLogs.write(f"creation de la commande{commande.id} en attente le {commande.dateCommande.strftime('%d/%m/%Y %H:%M')} \
par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode==2:
            self.commandeLogs.write(f"modification de la commande{commande.id} en attente le {datetime.now().strftime('%d/%m/%Y %H:%M')} \
par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode==3:
            self.commandeLogs.write(f"supression de la commande{commande.id} en attente le {datetime.now().strftime('%d/%m/%Y %H:%M')} \
par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        elif mode==4:
            self.commandeLogs.write(f"validation de la commande{commande.id} en attente le {datetime.now().strftime('%d/%m/%Y %H:%M')} \
par ({utilisateur.nom} {utilisateur.prenom} {utilisateur.telephone})\n")
        self.fermeture()

    def logStock(self, boisson, quantite, stock):
        self.stockLogs.write(f"ajout de {quantite} unite de {boisson.nom} le {datetime.now().strftime('%d/%m/%Y %H:%M')} stock actuel: {stock}\n")
        self.fermeture()

            
    def fermeture(self):
        self.clientLogs.close() if self.clientLogs else ...
        self.employeLogs.close() if self.employeLogs else ...
        self.connexionLogs.close() if self.connexionLogs else ... 
        self.commandeLogs.close() if self.commandeLogs else ... 
        self.categorieLogs.close() if self.categorieLogs else ...
        self.boissonLogs.close() if self.boissonLogs else ...

