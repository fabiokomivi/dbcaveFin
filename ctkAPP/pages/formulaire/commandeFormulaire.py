import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from controleur.boissonControler import *
from controleur.commandeControler import *
from controleur.ligneCommandeControler import *
from controleur.clientControler import obtenirClientparAttribue
from .erreur.erreur import erreur
from PIL import Image
import re
from .choisirClient import choixClient
from .choisirBoisson import choixBoisson
from .erreur.erreur import erreur

class commandeForm(ctk.CTkToplevel):

    commandeAttribue = ("nom", "prix unitaire", "quantite", "prix total")
    

    def __init__(self, parent, commande=None):
        super().__init__(parent)

        self.geometry("710x450")
        self.resizable(False, False)
        self.title("commandes")
        self.protocol("WM_DELETE_WINDOW", self.annuler)
        self.attributes('-topmost', True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.contenu = ctk.CTkFrame(self)
        self.contenu.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.commandeTmp = commande

        self.initBody()

        self.wait_visibility()
        self.grab_set()


    def initBody(self):
        self.contenu.grid_rowconfigure(0, minsize=75)
        self.contenu.grid_rowconfigure(1, weight=1)
        self.contenu.grid_columnconfigure(0, weight=1)

        clientFrame = ctk.CTkFrame(self.contenu, height=60)
        clientFrame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        clientFrame.grid_propagate(False)
        clientFrame.grid_columnconfigure(0, minsize=75)
        clientFrame.grid_columnconfigure(1, weight=1)
        clientFrame.grid_rowconfigure(0, weight=1)

        clientIdentite = ctk.CTkFrame(clientFrame)
        clientIdentite.grid_rowconfigure(0, minsize=20)
        clientIdentite.grid_rowconfigure(1, weight=1)

        for i in range(3):
            clientIdentite.grid_columnconfigure(i, weight=1)
                
        ctk.CTkLabel(clientIdentite, text="client", fg_color="#D9D9D9", height=10, corner_radius=6).grid(row=0, column=0, columnspan=3, padx=3, pady=3, sticky="ew")
                

        clientIdentite.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")

        ctk.CTkButton(clientFrame, text="choisir un client", fg_color="#00AA00", command=self.choisirClient).grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.labelNom = ctk.CTkLabel(clientIdentite, text="nom")
        self.labelPrenom = ctk.CTkLabel(clientIdentite, text="prenom")
        self.labelTelephone = ctk.CTkLabel(clientIdentite, text="telephone")

        self.labelNom.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")
        self.labelPrenom.grid(row=1, column=1, padx=3, pady=3, sticky="nsew")
        self.labelTelephone.grid(row=1, column=2, padx=3, pady=3, sticky="nsew")

        commandeFrame = ctk.CTkFrame(self.contenu)
        commandeFrame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        commandeFrame.grid_columnconfigure(0, weight=1)
        commandeFrame.grid_rowconfigure(0, minsize=50)
        commandeFrame.grid_rowconfigure(1, weight=1)


        controlFrame = ctk.CTkFrame(commandeFrame, height=75)
        controlFrame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton  (controlFrame, text="ajouter", fg_color="#00AA00", command=self.ajouterBoisson).pack(side="left", padx=5, pady=5)
        ctk.CTkButton  (controlFrame, text="modifier", fg_color="#00AA00", command=self.modifierLigneCommande).pack(side="left", padx=5, pady=5)
        ctk.CTkButton  (controlFrame, text="supprimer", fg_color="red", command=self.supprimerLigneCommande).pack(side="left", padx=5, pady=5)
        ctk.CTkButton  (controlFrame, text="valider", fg_color="green", command=self.valider).pack(side="right", padx=5, pady=5)

        style = tk.ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 14))  # Augmenter la taille de la police
        style.configure("mystyle.Treeview.Heading", font=("Arial", 16, "bold"))  # Augmenter la taille de la police des titres
        style.configure("mystyle.Treeview", rowheight=30)  # Augmenter la hauteur des lignes

        self.ligneCommandeTab = tk.ttk.Treeview(commandeFrame,style="mystyle.Treeview", columns=self.commandeAttribue, show="headings")
        self.ligneCommandeTab.grid(row=1, column=0, sticky="nsew")
        for attribue in self.commandeAttribue:
            self.ligneCommandeTab.heading(attribue, text=attribue)
            self.ligneCommandeTab.column(attribue, width=100)

        self.miseAjour()



    def choisirClient(self):
        if self.commandeTmp.estConnue():
            self.wait_window(erreur(self, "client non modifiable\nen mode modification"))
        else:
            self.wait_window(choixClient(self, self.commandeTmp))
            if self.commandeTmp.clientId:
                client = obtenirClientparAttribue(self.commandeTmp.clientId)
                self.labelNom.configure(text=client.nom)
                self.labelPrenom.configure(text=client.prenom)
                self.labelTelephone.configure(text=client.telephone)

    def ajouterBoisson(self):
        self.commandeTmp.ligneCourrante = None
        self.wait_window(choixBoisson(self, self.commandeTmp))
        if self.commandeTmp.ligneCourrante is not None:
            boisson = obtenirBoissonParAttribue(boissonId=self.commandeTmp.ligneCourrante.boissonId)
            self.ligneCommandeTab.insert("", tk.END,
                                         iid=self.commandeTmp.ligneCourrante.id,
                                         values=(boisson.nom,
                                                 boisson.prix,
                                                 self.commandeTmp.ligneCourrante.quantite,
                                                 boisson.prix*self.commandeTmp.ligneCourrante.quantite))
            if not self.commandeTmp.ligneCourrante.estConnue():
                self.commandeTmp.ajouteLigneInconnue(self.commandeTmp.ligneCourrante)
            self.commandeTmp.ligneCourrante = None
        
        # Réinitialiser la ligne courante
        self.commandeTmp.ligneCourrante = None

    def modifierLigneCommande(self):
        selection = self.ligneCommandeTab.selection()
        if selection:
            ligne_id = selection[0]
            
            if ligne_id in self.commandeTmp.idConnues:
                for ligne in self.commandeTmp.lignesConnues:
                    if ligne_id == str(ligne.id):
                        self.commandeTmp.ligneCourrante = ligne
                        break
            else:
                for ligne in self.commandeTmp.lignesInconnues:
                    if ligne_id == str(ligne.id):
                        self.commandeTmp.ligneCourrante = ligne
                        break

            self.wait_window(choixBoisson(self, self.commandeTmp))

            if self.commandeTmp.ligneCourrante is not None:
                if self.commandeTmp.ligneCourrante.modifie:
                    boisson = obtenirBoissonParAttribue(boissonId=self.commandeTmp.ligneCourrante.boissonId)
                    self.ligneCommandeTab.item(
                        ligne_id,
                        values=(
                            boisson.nom,
                            boisson.prix,
                            self.commandeTmp.ligneCourrante.quantite,
                            boisson.prix * self.commandeTmp.ligneCourrante.quantite
                        )
                    )
                    self.commandeTmp.ligneCourrante.modifie = True
        else:
            self.wait_window(erreur(self, "veuillez selectionner\nune ligne"))


    def supprimerLigneCommande(self):

        selection = self.ligneCommandeTab.selection()
        
        if selection:
            ligne_id = selection[0]

            self.ligneCommandeTab.delete(ligne_id)

            if ligne_id in self.commandeTmp.idConnues:
                for ligne in self.commandeTmp.lignesConnues:
                    if str(ligne.id) == ligne_id:
                        self.commandeTmp.supprimerLigne(ligne)
                        break

            elif ligne_id in self.commandeTmp.idInconnues:
                for ligne in self.commandeTmp.lignesInconnues:
                    if str(ligne.id) == ligne_id:
                        self.commandeTmp.supprimerLigne(ligne)
                        break
                
            if self.commandeTmp.ligneCourrante and str(self.commandeTmp.ligneCourrante.id) == ligne_id:
                self.commandeTmp.ligneCourrante = None
        else:
            self.wait_window(erreur(self, "veuillez selectionner\nune ligne"))


    def valider(self):
        if self.commandeTmp.clientId is None:
            message = "veuillez selectioner\nun client"
            self.wait_window(erreur(self, message=message))
        elif len(self.ligneCommandeTab.get_children())==0:
            message = "veuillez effectuer\nune commande"
            self.wait_window(erreur(self, message=message))
        else:
            self.commandeTmp.finaliser()
            self.destroy()

    def annuler(self):
        self.destroy()


    def miseAjour(self):
        if self.commandeTmp.estConnue():
            client = obtenirClientparAttribue(self.commandeTmp.clientId)
            self.labelNom.configure(text=client.nom)
            self.labelPrenom.configure(text=client.prenom)
            self.labelTelephone.configure(text=client.telephone)
            for ligne in self.commandeTmp.lignesConnues:
                boisson = obtenirBoissonParAttribue(boissonId=ligne.boissonId)
                self.ligneCommandeTab.insert("", tk.END, iid=ligne.id, values=(boisson.nom, boisson.prix, ligne.quantite, boisson.prix*ligne.quantite))
                ligne.modifie = True



            