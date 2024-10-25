import time
import customtkinter as ctk
import tkinter as tk
from .erreur.erreur import erreur
import re
from controleur.chefControler import creerChef
import hashlib


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("/home/fabio/Bureau/python/appCTKenv/ctkAPP/themes/myBlue.json")  # Thème bleue

class PremiereConnexion(ctk.CTkToplevel):
    emailPattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    numeroPattern = r"[0-9]{8}"
    nomPattern = r"[a-zA-Z]"
    mdpParttern = r"[a-zA-Z0-9@$!%*?&]+"


    def __init__(self, parent, callback):
        super().__init__(parent)
        self.geometry("345x380")
        self.resizable(False, False)
        self.title("")
        self.protocol("WM_DELETE_WINDOW", self.fermetureAnormale)
        self.attributes('-topmost', True)
        self.callback = callback
        self.controller = parent
 
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)


        self.contenu = ctk.CTkFrame(self)
        for i in range(7):
            self.contenu.grid_rowconfigure(i, weight=1)

        self.contenu.grid_columnconfigure(0, weight=1)

        self.contenu.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        ctk.CTkLabel(self.contenu, text="nouvel administrateur", font=ctk.CTkFont("Arial", size=25, weight="bold")).grid(row=0, column=0, pady=10, padx=5)
        self.entreeNom = ctk.CTkEntry(self.contenu, placeholder_text="nom", width=300)
        self.entreePrenom = ctk.CTkEntry(self.contenu, placeholder_text="prenom", width=300)
        self.entreeTelephone = ctk.CTkEntry(self.contenu, placeholder_text="telephone", width=300)
        self.entreeAddresse = ctk.CTkEntry(self.contenu, placeholder_text="addresse", width=300)
        self.entreeMdp = ctk.CTkEntry(self.contenu, placeholder_text="mot de passe", width=300)
        self.entreeMdpConfirm = ctk.CTkEntry(self.contenu, placeholder_text="confirmer", width=300)

        self.entreeNom.grid(row=1, column=0, pady=(10, 5))
        self.entreePrenom.grid(row=2, column=0, pady=(5, 5))
        self.entreeTelephone.grid(row=3, column=0, pady=(5, 5))
        self.entreeAddresse.grid(row=4, column=0, pady=(5, 5))
        self.entreeMdp.grid(row=5, column=0, pady=(5, 5))
        self.entreeMdpConfirm.grid(row=6, column=0, pady=(5, 10))

        self.confirmationFrame = ctk.CTkFrame(self, height=50)
        self.confirmationFrame.grid(row=1, column=0, sticky="ew", pady=5, padx=10)

        ctk.CTkButton(self.confirmationFrame, text="valider", fg_color="green", command=self.verification).pack(side="right", padx=(10, 10), pady=10)
        ctk.CTkButton(self.confirmationFrame, text="annuler", fg_color="red", command=self.fermetureAnormale).pack(side="left", padx=(10, 10), pady=10)

        self.wait_visibility()
        self.grab_set()

    def verification(self):
        nom = self.entreeNom.get().strip()
        prenom = self.entreePrenom.get().strip()
        telephone = self.entreeTelephone.get().strip()
        email = self.entreeAddresse.get().strip()
        mdp = self.entreeMdp.get().strip()
        mdpConfirm = self.entreeMdpConfirm.get().strip()

        if not re.match(self.nomPattern, nom):
            self.rougir(self.entreeNom)
        elif not re.match(self.nomPattern, prenom):
            self.rougir(self.entreePrenom)
        elif not re.match(self.numeroPattern, telephone):
            self.rougir(self.entreeTelephone)
        elif not re.match(self.emailPattern, email):
            self.rougir(self.entreeAddresse)
        elif not re.match(self.mdpParttern, mdp):
            self.rougir(self.entreeMdp)
        elif not re.match(self.mdpParttern, mdpConfirm):
            self.rougir(self.entreeMdpConfirm)
        elif mdp != mdpConfirm:
            message = "les mots de passe entres\nne sont pas identiques"
            self.controller.wait_window(erreur(self.controller, message))
        else:
            self.callback({"nom":nom, "prenom":prenom, "motDePasse":self.hasher(mdp), "telephone":telephone, "email": email})
            self.destroy()

    def fermetureAnormale(self):
        self.callback({})
        self.destroy()

    def info(self):
        print(f"width: {self.winfo_width()}, height: {self.winfo_height()}")

    def rougir(self, widget):
        widget.configure(fg_color = "red")
        self.after(1500, lambda:self.blanchir(widget))

    def blanchir(self, widget):
        widget.configure(fg_color="white")

    def hasher(self, password):
        passwordBytes = password.encode('utf-8')
        passwordHash = hashlib.sha256(passwordBytes)
        return passwordHash.hexdigest()