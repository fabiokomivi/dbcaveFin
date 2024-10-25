import customtkinter as ctk
import tkinter as tk
from PIL import Image
from controleur.clientControler import obtenirClientParEmploye
from controleur.chefControler import modifierChef, obtenirChefPar
import re
import hashlib
from .formulaire.erreur.erreur import erreur
ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue

class ParametreGerantPage(ctk.CTkFrame):

    image = Image.open("ctkAPP/images/chef.png")
    userImage = ctk.CTkImage(light_image=image, dark_image=image, size=(100, 100))
    mdpPattern = r"[a-zA-Z0-9@$!%*?&]+"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, minsize=200)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=100)
        self.grid_columnconfigure(2, minsize=300)

        topFrameLeft = ctk.CTkFrame(self)
        topFrameLeft.grid_propagate(False)
        topFrameLeft.grid(row=0, column=0, padx=5,pady=5, sticky="ew")

        topFrameLeft.grid_columnconfigure(0, minsize=200)
        topFrameLeft.grid_columnconfigure(1, weight=1)
        topFrameLeft.grid_rowconfigure(0, weight=1)
        topFrameLeft.grid_rowconfigure(1, weight=1)
        topFrameLeft.grid_rowconfigure(2, weight=1)
        topFrameLeft.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(topFrameLeft, text="", image=self.userImage).grid(row=0, column=0, rowspan=4, padx=3, pady=3, sticky="nsew")
        self.nomLabel = ctk.CTkLabel(topFrameLeft, text="nom", anchor="w")
        self.prenomLabel = ctk.CTkLabel(topFrameLeft, text="prenom", anchor="w")
        self.telephoneLabel = ctk.CTkLabel(topFrameLeft, text="telephone", anchor="w")
        self.emailLabel = ctk.CTkLabel(topFrameLeft, text="email", anchor="w")

        self.nomLabel.grid(row=0, column=1, padx=3, pady=2, sticky="ew")
        self.prenomLabel.grid(row=1, column=1, padx=3, pady=2, sticky="ew")
        self.telephoneLabel.grid(row=2, column=1, padx=3, pady=2, sticky="ew")
        self.emailLabel.grid(row=3, column=1, padx=3, pady=2, sticky="ew")


        topFrameMiddle = ctk.CTkFrame(self)
        topFrameMiddle.grid_propagate(False)
        topFrameMiddle.grid(row=0, column=1, padx=5,pady=5, sticky="ew")

        topFrameMiddle.grid_rowconfigure(0, minsize=25)
        topFrameMiddle.grid_rowconfigure(1, weight=1)

        topFrameMiddle.grid_columnconfigure(0, weight=1)
        topFrameMiddle.grid_columnconfigure(1, weight=1)
        topFrameMiddle.grid_columnconfigure(2, weight=1)

        topFrameMiddle.grid_propagate(False)

        ctk.CTkLabel(topFrameMiddle, text="theme", font=ctk.CTkFont("Arial", size=20, weight="bold")).grid(row=0, column=0, columnspan=3, sticky="ew")
        ctk.CTkLabel(topFrameMiddle, text="    clair   ", width=50, anchor="e", font=ctk.CTkFont("Arial", size=15, weight="bold")).grid(row=1, column=0, sticky="ew")
        ctk.CTkSwitch(topFrameMiddle, text="", width=20,command=controller.setTheme).grid(row=1, column=1, sticky="nsew")
        ctk.CTkLabel(topFrameMiddle, text="sombre  ", width=40, font=ctk.CTkFont("Arial", size=15, weight="bold"), anchor="w").grid(row=1, column=2, sticky="ew")


        topFrameRight = ctk.CTkFrame(self)
        topFrameRight.grid_propagate(False)
        topFrameRight.grid(row=0, column=2, padx=5,pady=5, sticky="ew")

        topFrameRight.grid_columnconfigure(0, weight=1)
        topFrameRight.grid_rowconfigure(0, minsize=30)
        topFrameRight.grid_rowconfigure(1, minsize=30)
        topFrameRight.grid_rowconfigure(2, minsize=30)
        topFrameRight.grid_rowconfigure(3, minsize=30)
        topFrameRight.grid_rowconfigure(4, minsize=30)
        topFrameRight.grid_rowconfigure(5, minsize=30)

        ctk.CTkLabel(topFrameRight, text="securite", font=ctk.CTkFont("Arial", size=20, weight="bold"), width=250).grid(row=0, column=0, padx=3)
        ctk.CTkLabel(topFrameRight, text="changer mon mot de passe", font=ctk.CTkFont("Arial", size=15, weight="bold"), width=250).grid(row=1, column=0, padx=3)
        self.mpdEntree = ctk.CTkEntry(topFrameRight, placeholder_text="mot de passe actuel", width=250)
        self.mpdNouvEntree = ctk.CTkEntry(topFrameRight, placeholder_text="nouveau mot de passe", width=250)
        self.mpdConfEntree = ctk.CTkEntry(topFrameRight, placeholder_text="confirmer mot de passe", width=250)
        self.mpdEntree.grid(row=2, column=0, padx=3, pady=2)
        self.mpdNouvEntree.grid(row=3, column=0, padx=3, pady=2)
        self.mpdConfEntree.grid(row=4, column=0, padx=3, pady=2)
        ctk.CTkButton(topFrameRight, text="valider", fg_color="green", command=self.verification).grid(row=5, column=0, padx=3, pady=2)


        self.miseAjour()



    
    def miseAjour(self):
        self.miseAjourEmploye()

    def miseAjourEmploye(self):
        if self.controller.utilisateurCourant:
            self.nomLabel.configure(text=self.controller.utilisateurCourant.nom)
            self.prenomLabel.configure(text=self.controller.utilisateurCourant.prenom)
            self.telephoneLabel.configure(text=self.controller.utilisateurCourant.telephone)
            self.emailLabel.configure(text=self.controller.utilisateurCourant.addresse)

    def verification(self):
        mdp = self.mpdEntree.get().strip()
        mdpNouv = self.mpdNouvEntree.get().strip()
        mdpConf = self.mpdConfEntree.get().strip()
        if not re.match(self.mdpPattern, mdp):
            self.rougir(self.mpdEntree)

            self.wait_window(erreur(self.controller, "mot de passe invalide"))
        elif not re.match(self.mdpPattern, mdpNouv):
            self.rougir(self.mpdNouvEntree)

            self.wait_window(erreur(self.controller, "mot de passe invalide"))
        elif not re.match(self.mdpPattern, mdpConf):
            self.rougir(self.mpdConfEntree)
            self.wait_window(erreur(self.controller, "mot de passe invalide"))

        elif mdpConf != mdpNouv:
            self.wait_window(erreur(self.controller, "les mots de passe\nsont differents"))

        elif self.hasher(mdp) != self.controller.utilisateurCourant.motDePasse:
           self.wait_window(erreur(self.controller, "le mot de passe actuel\nest incorrect"))

        else:
            
            modifierChef(addresse=self.controller.utilisateurCourant.addresse, password=mdpNouv)
            self.controller.utilisateurCourant = obtenirChefPar(id=self.controller.utilisateurCourant.id)
            self.wait_window(erreur(self.controller, "mot de passe modifié\navec succès"))
            self.miseAjour()
            self.vider()


    def rougir(self, widget):
        widget.configure(fg_color = "red")
        self.after(1500, lambda:self.blanchir(widget))

    def blanchir(self, widget):
        widget.configure(fg_color="white")

    def hasher(self, password):
        passwordBytes = password.encode('utf-8')
        passwordHash = hashlib.sha256(passwordBytes)
        return passwordHash.hexdigest()
    
    def vider(self):
        self.mpdEntree.delete(0, tk.END)
        self.mpdNouvEntree.delete(0, tk.END)
        self.mpdConfEntree.delete(0, tk.END)
