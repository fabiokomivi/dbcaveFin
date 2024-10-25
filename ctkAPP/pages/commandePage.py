import datetime
import customtkinter as ctk
import tkinter as tk
from PIL import Image
from .formulaire.commandeFormulaire import commandeForm
from controleur.commandeControler import *
from controleur.clientControler import *
from controleur.employeControler import *
from controleur.ligneCommandeControler import *
from controleur.boissonControler import obtenirBoissonParAttribue, mettreAjourBoisson
from .formulaire.erreur.erreur import erreur
from .formulaire.erreur.confirmation import Confirmation
from weasyprint import CSS, HTML
from .formulaire.temp.temp import *
from pages.journalisation.log import logs


ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue

class CommandePage(ctk.CTkFrame):

    commandeAttribue = ("nom", "prenom", "telephone", "date", "montant", "etat")
    rechecheImagePath = "ctkAPP/images/recherche.png"
    reponse = {}


    def __init__(self, parent, controller):
        super().__init__(parent)
    
        ctk.CTkLabel(self, text="commande").grid(row=0, column=0)

        self.controller = controller
        self.autorisation = False
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=1)


        self.titre = ctk.CTkLabel(self, text="commandes", font=ctk.CTkFont(family="Arial", size=25, weight="bold"), height=30)
        self.menu = ctk.CTkFrame(self, height=150)
        self.tabFrame = ctk.CTkFrame(self)
        
        self.titre.grid(row=0, column=0)
        self.menu.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 5))
        self.tabFrame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(5, 5))

        ctk.CTkButton(self.menu, text="nouveau", fg_color="green", height=35, width=50, command=self.ajouterCommande).pack(side="left", padx=3, pady=3)
        ctk.CTkButton(self.menu, text="modifier", fg_color="#00AA00", height=35, width=50, command=self.modifierCommande).pack(side="left", padx=3, pady=3)
        ctk.CTkButton(self.menu, text="valider", fg_color="#00AA00", height=35, width=50, command=self.validerCommande).pack(side="left", padx=3, pady=3)
        ctk.CTkButton(self.menu, text="facture", fg_color="#00AA00", height=35, width=50, command=self.creerFacture).pack(side="left", padx=3, pady=3)
        ctk.CTkButton(self.menu, text="supprimer", fg_color="red", height=35, width=50, command=self.supprimerCommande).pack(side="right", padx=3, pady=3)
        

        self.tabFrame.grid_columnconfigure(0, weight=1)
        self.tabFrame.grid_rowconfigure(1, weight=1)
        self.tabFrame.grid_rowconfigure(0, weight=0)

        style = tk.ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 14))  # Augmenter la taille de la police
        style.configure("mystyle.Treeview.Heading", font=("Arial", 16, "bold"))  # Augmenter la taille de la police des titres
        style.configure("mystyle.Treeview", rowheight=30)  # Augmenter la hauteur des lignes

        self.barreRecherche = ctk.CTkFrame(self.tabFrame, height=50)
        self.commandeTab = tk.ttk.Treeview(self.tabFrame, style="mystyle.Treeview", columns=self.commandeAttribue, show="headings")
        

        for attribue in self.commandeAttribue:
            self.commandeTab.heading(attribue, text=attribue)
            self.commandeTab.column(attribue, width=100)

        self.barreRecherche.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.commandeTab.grid(row=1, column=0, sticky="nsew")
        self.barreRecherche.grid_columnconfigure(0, weight=1)
        self.boxRecherche = ctk.CTkFrame(self.barreRecherche, width=300, height=50)
        self.boxRecherche.grid(row=0, column=0, pady=2)

        self.selecteur = ctk.CTkComboBox(self.boxRecherche, values=("nom", "prenom", "telephone"))
        self.selecteur.set(self.commandeAttribue[0])

        ctk.CTkLabel(self.boxRecherche, text="", image=ctk.CTkImage(Image.open(self.rechecheImagePath))).pack(padx=2, pady=2, side="right")

        self.rechercheEntree = ctk.CTkEntry(self.boxRecherche, width=200)
        self.rechercheEntree.pack(padx=2, pady=2, side="right")
        self.rechercheEntree.bind("<KeyRelease>", self.recherche)

        self.selecteur.pack(side="left", padx=2, pady=2)
        self.miseAjour()

        
    def miseAjour(self):
        if self.grid_info():
            self.controller.title("commande")
        commandes = obtenirCommandePar(tous=True)
        self.commandeTab.delete(*self.commandeTab.get_children())
        for commande in commandes:
            client = commande.client
            montant = 0
            for lignecommande in commande.lignesCommande:
                montant += lignecommande.quantite*lignecommande.boisson.prix
            self.commandeTab.insert("", tk.END, iid=commande.id, values=(client.nom, client.prenom, client.telephone, commande.dateCommande.strftime('%H:%M %d/%m/%Y'), montant, commande.etat))
            

    def recherche(self, event=None):
        critere = self.selecteur.get()
        texteRechere = self.rechercheEntree.get()
        self.commandeTab.delete(*self.commandeTab.get_children())
        match critere:
            case "id":
                clients = obtenirClientparAttribue(employeId=eval(texteRechere.strip()))
            case "nom":
                clients = obtenirClientparAttribue(nom=texteRechere)
            case "prenom":
                clients = obtenirClientparAttribue(prenom=texteRechere)
            case "telephone":
                clients = obtenirClientparAttribue(telephone=texteRechere)
            case "":
                clients = obtenirClientparAttribue(tous=True)
        for client in clients:  
            commandes = obtenirCommandePar(clientId=client.id)   
            for commande in commandes:
                if commande:
                    montant = 0
                    for detail in commande.lignesCommande:
                        montant += detail.quantite*detail.prix
                        self.commandeTab.insert("", tk.END, iid=commande.id, values=(client.nom, client.prenom, client.telephone, commande.dateCommande.strftime('%H:%M %d/%m/%Y'), montant, commande.etat))

    def ajouterCommande(self):
        self.commandeTmp = CommandeTmp(connue=False)
        self.wait_window(commandeForm(self.controller, self.commandeTmp))
        self.ajoutOuMiseAjour()

        
    def modifierCommande(self):
        selection = self.commandeTab.selection()
        if selection:
            commande = obtenirCommandePar(commandeId=selection[0])
            if commande.etat == "validée":
                message = "impossible de modifier\nune commande validée"
                self.wait_window(erreur(self.controller, message=message))
            else:
                client = obtenirClientparAttribue(clientId=commande.clientId)
                employe = obtenirEmployePar(id=commande.employeId)

                self.commandeTmp = CommandeTmp(id=commande.id, clientId=client.id, employeId=employe.id, date=commande.dateCommande, connue=True)
                for ligne in commande.lignesCommande:
                    self.commandeTmp.ajouteLigneConnue(LigneCommandeTmp(id=ligne.id,
                                                                        boissonId=ligne.boissonId,
                                                                        quantite=ligne.quantite,
                                                                        connue=True))
                    
                self.wait_window(commandeForm(self.controller, self.commandeTmp))
                self.ajoutOuMiseAjour()

    def ajoutOuMiseAjour(self):
        if self.commandeTmp.finalise:
            if not self.commandeTmp.estConnue():
                commande = creerCommande(clientId=self.commandeTmp.clientId,
                                        employeId=self.controller.utilisateurCourant.id)
                self.commandeTmp.id = commande.id

            for ligne in self.commandeTmp.lignesConnuesSupprimes:
                SupprimerLigneCommande(ligne.id)

            for ligne in self.commandeTmp.lignesConnues:
                ModifierLigneCommande(ligneCommandeId=ligne.id,
                                    nouvelleQuantite=ligne.quantite)

            if self.commandeTmp.lignesInconnues:
                for ligne in self.commandeTmp.lignesInconnues:
                    AjouterLigneCommande(commandeId=self.commandeTmp.id,
                                        boissonId=ligne.boissonId,
                                        quantite=ligne.quantite,
                                        prix=ligne.prix,
                                        prixTotal=ligne.quantite * ligne.prix)

            commande = obtenirCommandePar(commandeId=self.commandeTmp.id)
            client = obtenirClientparAttribue(clientId=self.commandeTmp.clientId)

            if self.commandeTmp.estConnue():
                self.commandeTab.item(commande.id,
                                    values=(client.nom, client.prenom, client.telephone,
                                            commande.dateCommande.strftime('%H:%M %d/%m/%Y'),
                                            commande.prixTotal(),
                                            commande.etat))
                logs().logCommande(commande, self.controller.utilisateurCourant, mode=2)
                message = "commande modifiée\navec succès"
                self.wait_window(erreur(self.controller, message=message))
            else:
                self.commandeTab.insert("",
                                        tk.END,
                                        iid=commande.id,
                                        values=(client.nom, client.prenom, client.telephone,
                                                commande.dateCommande.strftime('%H:%M %d/%m/%Y'),
                                                commande.prixTotal(),
                                                commande.etat))
                logs().logCommande(commande, self.controller.utilisateurCourant, mode=1)
                message = "commande enregistrée\navec succès"
                self.wait_window(erreur(self.controller, message=message))
        else:
            message = "commande non enregistrée" if not self.commandeTmp.estConnue() else "commande non modifiée"
            self.wait_window(erreur(self.controller, message=message))

    def supprimerCommande(self):
        selection = self.commandeTab.selection()
        commande = obtenirCommandePar(commandeId=selection[0])
        if commande.etat=="validée":
            message = "impossible de\nsupprimer une commande\nvalidée"
            self.wait_window(erreur(self.controller, message=message))
        else:
            message = "voulez vous vraiment\nsupprimer la commande?"
            self.wait_window(Confirmation(self.controller, message=message, callback=self.avoirAutorisation))
            if self.autorisation:
                if selection:
                    logs().logCommande(commande, self.controller.utilisateurCourant, mode=3)
                    if supprimerCommande(selection[0]):
                        self.commandeTab.delete(selection)
    
    def validerCommande(self):
            
            selection = self.commandeTab.selection()
            if selection:
                commande = obtenirCommandePar(commandeId=selection[0])
                if commande.etat=="validée":
                    message = "commande déjà\nvalidée"
                    self.wait_window(erreur(self.controller, message=message))
                else:
                    message = "voulez vous vraiment\nvalider la commande?"
                    self.wait_window(Confirmation(self.controller, message=message, callback=self.avoirAutorisation))
                    if self.autorisation:
                        for ligne in commande.lignesCommande:
                            boisson = obtenirBoissonParAttribue(boissonId=ligne.boissonId)
                            if boisson.stock.quantite < ligne.quantite:
                                message = (f"Quantité insuffisante pour {boisson.nom}.\n"
                                    f"Quantité demandée : {ligne.quantite}\n"
                                    f"Quantité disponible : {boisson.stock.quantite}\n"
                                    f"veuillez modifier la commande")
                                self.wait_window(erreur(self.controller, message=message))
                                return
                        for ligne in commande.lignesCommande:
                            mettreAjourBoisson(ligne.boissonId, ligne.quantite)
                        validerCommande(commandeId=commande.id)
                        client = obtenirClientparAttribue(clientId=commande.clientId)
                        self.commandeTab.item(commande.id,
                                                values=(client.nom, client.prenom, client.telephone,
                                                        commande.dateCommande.strftime('%H:%M %d/%m/%Y'),
                                                        commande.prixTotal(),
                                                        "validée"))
                        logs().logCommande(commande, self.controller.utilisateurCourant, mode=4)
                        message = "commande validée\navec succeès"
                        self.wait_window(erreur(self.controller, message=message))
            else:
                message = "veuillez selectioner\nune commande"
                self.wait_window(erreur(self.controller, message=message))
                
    def avoirAutorisation(self, permission):
        self.autorisation = permission


        

                

    def creerFacture(self):
        selection = self.commandeTab.selection()
        if selection:
            commande = obtenirCommandePar(commandeId=selection[0])
            if commande.etat == "en attente":
                self.wait_window(erreur(self.controller, "veuillez d'abord\nvalider la\ncommande"))
            elif commande.etat == "validée":
                client = commande.client
                details = commande.lignesCommande

                factureHtml = f"""
                <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                margin: 0;
                                padding: 0;
                            }}
                            .container {{
                                width: 95%;
                                margin: 0 auto;
                                padding: 5px;
                            }}
                            .header {{
                                text-align: center;
                                font-size: 24px;
                                font-weight: bold;
                                margin-bottom: 40px;
                            }}
                            .client-date {{
                                display: flex;
                                justify-content: space-between;
                                margin-bottom: 20px;
                            }}
                            .client-info {{
                                float: left;
                            }}
                            .date-info {{
                                text-align: right;
                            }}
                            .clearfix {{
                                clear: both;
                            }}
                            table {{
                                width: 100%;
                                border-collapse: collapse;
                                margin-top: 20px;
                            }}
                            table, th, td {{
                                border: 1px solid black;
                            }}
                            th, td {{
                                padding: 10px;
                                text-align: center;
                            }}
                            th {{
                                background-color: #f2f2f2;
                            }}
                            tfoot td {{
                                font-weight: bold;
                            }}
                            .total {{
                                margin-top: 20px;
                                text-align: right;
                                font-size: 18px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                FACTURE N°{commande.id}
                            </div>
                            <div class="client-date">
                                <div class="client-info">
                                    <p>Nom: {client.nom}</p>
                                    <p>Prénom: {client.prenom}</p>
                                    <p>Téléphone: {client.telephone}</p>
                                    <p>Adresse: {client.addresse}</p>
                                </div>
                                <div class="date-info">
                                    <p>Date: {commande.dateCommande.strftime('%d/%m/%Y')}</p>
                                </div>
                            </div>

                            <table>
                                <thead>
                                    <tr>
                                        <th>Produit</th>
                                        <th>Quantité</th>
                                        <th>Prix Unitaire (FCFA)</th>
                                        <th>Total (FCFA)</th>
                                    </tr>
                                </thead>
                                <tbody>
                """
                for detail in details:
                    nom = detail.boisson.nom
                    quantite = detail.quantite
                    prix = detail.boisson.prix
                    prixTotal = detail.prixTotal
                    factureHtml += f"""
                                    <tr>
                                        <td>{nom}</td>
                                        <td>{quantite}</td>
                                        <td>{prix}</td>
                                        <td>{prixTotal}</td>
                                    </tr>
                    """
                total_general = sum(detail.quantite * detail.boisson.prix for detail in details)
                factureHtml += f"""
                                </tbody>
                                <tfoot>
                                    <tr>
                                        <td colspan="3">Total Général</td>
                                        <td>{total_general} FCFA</td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </body>
                </html>
                """
                html = HTML(string=factureHtml)
                html.write_pdf(f"ctkAPP/factures/facture_{commande.id}.pdf", stylesheets=[CSS(string='@page { size: A5; }')])
                self.wait_window(erreur(self, "facture generee avec succes"))


