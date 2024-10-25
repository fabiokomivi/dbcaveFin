import customtkinter as ctk
import tkinter as tk
from .erreur.erreur import erreur
import re
from controleur.categorieControler import *

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue

class categorieForm(ctk.CTkToplevel):

    nomPattern = r"[a-zA-Z]+"

    def __init__(self,controller, callback, dico, mode=False):
        super().__init__(controller)
        self.geometry("350x400")
        self.centreFenetre()
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.fermetureAnormale)
        self.attributes('-topmost', True)
        self.callback = callback
        self.mode = mode
        self.title("ajout categorie" if not self.mode else "modification categorie")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, minsize=50)


        self.contenu = ctk.CTkFrame(self)
        #for i in range(4):
        #    self.contenu.grid_rowconfigure(i, weight=1)
        self.contenu.grid_columnconfigure(0, weight=1)
        self.contenu.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.entreeNom = ctk.CTkEntry(self.contenu, placeholder_text="nom de categorie", width=300)
        self.entreeDescription = ctk.CTkTextbox(self.contenu, font=("Arial", 18), wrap="word", height=250, width=300)

        if dico:
            self.entreeNom.insert(0, dico["nom"])
            self.entreeDescription.insert("1.0", dico["description"])

        self.entreeNom.grid(row=0, column=0, pady=(10, 5))
        self.entreeDescription.grid(row=1, column=0, pady=(5, 10))


        self.confirmationFrame = ctk.CTkFrame(self, height=50)
        self.confirmationFrame.grid(row=2, column=0, sticky="ew", pady=10, padx=10)

        self.valider = ctk.CTkButton(self.confirmationFrame, text="valider", fg_color="green", command=self.verification)
        self.annuler = ctk.CTkButton(self.confirmationFrame, text="annuler", fg_color="red", command=self.fermetureAnormale)
        self.valider.pack(side="right", padx=10, pady=5)
        self.annuler.pack(side="left", padx=10, pady=5)

        self.wait_visibility()
        self.grab_set()
        self.focus_force()


    def verification(self):
        nom = self.entreeNom.get()
        description = self.entreeDescription.get("1.0", "end-1c")

        if not re.match(self.nomPattern, nom):
            self.rougir(self.entreeNom)
        else:
            if not self.mode:
                if obtenirCategorieParAttribue(nom=nom, categorieId="", description="", tous=False): 
                    self.wait_window(erreur(self, "cette categorie existe dejà"))
                else:
                    self.callback({"nom": nom, "description": description})
                    self.destroy()
            else:
                self.callback({"nom": nom, "description": description})
                self.destroy()

    def rougir(self, widget):
        widget.configure(fg_color = "red")
        self.after(1500, lambda:self.blanchir(widget))

    def blanchir(self, widget):
        widget.configure(fg_color="white")


    def fermetureAnormale(self):
        self.callback(None)
        self.destroy()

    def centreFenetre(self):

        pere_x = self.master.winfo_x()
        pere_y = self.master.winfo_y()
        pere_largeur = self.master.winfo_width()
        pere_hauter = self.master.winfo_height()

        enfant_largeur = self.winfo_reqwidth()
        enfant_hauteur = self.winfo_reqheight()

        position_x = pere_x + (pere_largeur // 2) - (enfant_largeur // 2)
        position_y = pere_y + (pere_hauter // 2) - (enfant_hauteur // 2)

        self.geometry(f"+{position_x}+{position_y}")
