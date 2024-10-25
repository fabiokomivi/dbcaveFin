import time
import customtkinter as ctk
from controleur.employeControler import *
from controleur.chefControler import *
import re
from PIL import Image
from .formulaire.erreur.erreur import erreur
from .formulaire.motDePasseOublier import motDePasseOublier
from pages.journalisation.log import logs



ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue

class ConnexionPage(ctk.CTkFrame):

    loginIMage = ctk.CTkImage(light_image=Image.open("ctkAPP/images/login.png"), dark_image=Image.open("ctkAPP/images/login.png"), size=(150, 150))
    
    patern = r"[a-zA-Z0-9#*@_]+"
    def __init__(self, parent, controller):
        super().__init__(parent)
        controller.title("connexion")
        self.controller = controller


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.connexionFrame = ctk.CTkFrame(self, height=550, width=500)
        self.connexionFrame.grid_propagate(False)
        self.connexionFrame.grid(row=0, column=0, pady=75)

        
        self.connexionFrame.grid_columnconfigure(0, weight=1)

        self.connexionFrame.grid_rowconfigure(0, weight=1)
        self.connexionFrame.grid_rowconfigure(1, minsize=50)
        self.connexionFrame.grid_rowconfigure(2, minsize=5)
        self.connexionFrame.grid_rowconfigure(3, minsize=50)
        self.connexionFrame.grid_rowconfigure(4, minsize=15)
        self.connexionFrame.grid_rowconfigure(5, minsize=50)
        self.connexionFrame.grid_rowconfigure(6, minsize=15)
        self.connexionFrame.grid_rowconfigure(7, weight=1)

        for i in range(3):
            self.connexionFrame.grid_rowconfigure(i, weight=1)
        self.connexionFrame.grid_columnconfigure(0, weight=1)
        

        ctk.CTkLabel(self.connexionFrame, text="", image=self.loginIMage, height=100, width=100, font=ctk.CTkFont(family="Arial", size=35, weight="bold"))\
            .grid(row=0, column=0,columnspan=2, padx=20, sticky="")
        
        ctk.CTkLabel(self.connexionFrame, text="connexion", font=ctk.CTkFont(family="Arial", size=35, weight="bold"))\
            .grid(row=1, column=0, padx=20,columnspan=2)
        

        userFrame = ctk.CTkFrame(self.connexionFrame, height=50, width=300, fg_color="transparent")
        userFrame.grid(row=2, column=0,rowspan=2, columnspan=2, pady=10)
        
        userLabel = ctk.CTkLabel(userFrame, text="nom", width=300, font=ctk.CTkFont(family="Arial", size=20, weight="bold"), anchor="sw")
        userLabel.grid(row=0, column=0, padx=0, sticky="")

        self.userEntree = ctk.CTkEntry(userFrame,font=ctk.CTkFont(family="Arial", size=20, weight="bold"), height=50, width=300)
        self.userEntree.grid(row=1, column=0, pady=0)

        ctk.CTkLabel(self.connexionFrame, text="mot de passe", width=300, font=ctk.CTkFont(family="Arial", size=20, weight="bold"), anchor="sw")\
            .grid(row=4, column=0, padx=20,columnspan=2, sticky="")

        passFrame = ctk.CTkFrame(self.connexionFrame, height=50, width=300, fg_color="transparent")
        passFrame.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        passFrame.grid_columnconfigure(0, weight=1)
        passFrame.grid_columnconfigure(1, minsize=25)
        passFrame.grid_rowconfigure(0, weight=1)


        self.mpdEntree = ctk.CTkEntry(passFrame, font=ctk.CTkFont(family="Arial", size=20, weight="bold"), show="•", height=50, width=250)
        self.mpdEntree.grid(row=0, column=0, padx=2, pady=(0, 0))

        self.passState = ctk.CTkCheckBox(passFrame, text="🙈", width=50, height=25, onvalue=1, offvalue=0, command=self.changeEtatMpd)
        #self.changeEtatMpd()
        self.passState.grid(row=0, column=1, sticky="")

        self.boutonOublier = ctk.CTkButton(self.connexionFrame, width=300, text="mot de passe oublier", fg_color="transparent",hover="green", text_color="red",anchor="ne",command=self.motDePasseOublier)
        self.boutonOublier.grid(row=6, column=0,columnspan=2, pady=(0, 0))
        self.boutonOublier.bind("<Leave>", self.quitterBoutonOblier)
        self.boutonOublier.bind("<Enter>", self.entrerBoutonOblier)

        self.bouttonCommit = ctk.CTkButton(self.connexionFrame,width=200, height=20, text="valider", fg_color="green", text_color="white",command=self.verification)
        self.bouttonCommit.grid(row=7, column=0,columnspan=2, pady=(10, 10))


        self.userEntree.insert(0, "amouzou")


        self.mpdEntree.insert(0, "123")


    def changeEtatMpd(self):
        if self.passState.get():
            self.mpdEntree.configure(show="")
            self.passState.configure(text="👁")
        else:
            self.mpdEntree.configure(show="•")
            self.passState.configure(text="🙈")

    def motDePasseOublier(self):
        self.controller.wait_window(motDePasseOublier(self.controller))

    def quitterBoutonOblier(self, event):
        self.boutonOublier.configure(text_color="red")

    def entrerBoutonOblier(self, event):
        self.boutonOublier.configure(text_color="green")

        

    def verification(self):
        motDePasse = self.mpdEntree.get()
        nom = self.userEntree.get()
        if not re.match(self.patern, nom):
            self.rougir(self.userEntree)
            self.controller.wait_window(erreur(self.controller, "nom invalide"))

        elif not re.match(self.patern, motDePasse):
            self.rougir(self.mpdEntree)
            self.controller.wait_window(erreur(self.controller, "mot de passe invalide"))
        else:
            utilisateur = obtenirChefPar(nom=nom, motDePasse=motDePasse)
            
            if utilisateur:
                self.controller.utilisateurCourant=utilisateur
                logs().logConnexion(utilisateur)
                self.controller.wait_window(erreur(self.controller, "connexion reussie"))
                self.controller.title("dashboard")
                self.controller.pagesChef["dashboard"].miseAjour()
                self.controller.pagesChef["dashboard"].tkraise()
                self.controller.pagesSecondaire["gestions"].tkraise()
                self.controller.pagesPrimaire["contenu"].tkraise()
                self.viderChamp()
            else:
                utilisateur = obtenirEmployePar(nom=nom, mdp=motDePasse, connexion=True)
                if utilisateur:
                    self.controller.utilisateurCourant=utilisateur[0]
                    logs().logConnexion(utilisateur[0])
                    self.controller.wait_window(erreur(self.controller, "connexion reussie"))
                    self.controller.pagesEmploye["clients"].miseAjour()
                    self.controller.pagesEmploye["clients"].tkraise()
                    self.controller.pagesSecondaire["pageEmploye"].tkraise()
                    self.controller.pagesPrimaire["contenu"].tkraise()
                    self.controller.title("client")
                    self.controller.pagesSecondaire["pageEmploye"].tkraise()
                    self.viderChamp()
                else:
                    self.controller.wait_window(erreur(self.controller, "connexion echouée"))
    
    def rougir(self, widget):
        widget.configure(fg_color = "red")
        self.after(1500, lambda:self.blanchir(widget))

    def blanchir(self, widget):
        widget.configure(fg_color="white")

    def miseAjour(self):
        if self.grid_info():
            self.controller.title("connexion")

    def viderChamp(self):
        self.userEntree.delete(0, ctk.END)
        self.mpdEntree.delete(0, ctk.END) 

    

    

        