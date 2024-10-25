import time
import customtkinter as ctk
import tkinter as tk
from .erreur.erreur import erreur
import re
from controleur.clientControler import obtenirClientparAttribue


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("/home/fabio/Bureau/python/appCTKenv/ctkAPP/themes/myBlue.json")  # Thème bleue

class ClientForm(ctk.CTkToplevel):
    emailPattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    numeroPattern = r"^(\d{8}|)$"
    nomPattern = r"[a-zA-Z]"

    def __init__(self,controller, callback, infoClient, mode=False):
        super().__init__(controller)
        self.geometry("319x247")
        self.resizable(False, False)
        self.title("ajouter client" if not mode else "modifier client")
        self.protocol("WM_DELETE_WINDOW", self.fermetureAnormale)
        self.attributes('-topmost', True)
        self.callback = callback
        self.mode = mode
        self.infoClient = infoClient
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, minsize=50)


        self.contenu = ctk.CTkFrame(self)

        self.contenu.grid_columnconfigure(0, weight=1)
        self.contenu.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.entreeNom = ctk.CTkEntry(self.contenu, placeholder_text="nom", width=250)
        self.entreePrenom = ctk.CTkEntry(self.contenu, placeholder_text="prenom", width=250)
        self.entreeTelephone = ctk.CTkEntry(self.contenu, placeholder_text="telephone", width=250)
        self.entreeAddresse = ctk.CTkEntry(self.contenu, placeholder_text="addresse", width=250)

        if infoClient:
            self.entreeNom.insert(0, infoClient["nom"])
            self.entreePrenom.insert(0, infoClient["prenom"])
            self.entreeTelephone.insert(0, infoClient["telephone"])
            self.entreeAddresse.insert(0, infoClient["addresse"])

        self.entreeNom.grid(row=0, column=0, pady=(10, 5))
        self.entreePrenom.grid(row=1, column=0, pady=(5, 5))
        self.entreeTelephone.grid(row=2, column=0, pady=(5, 5))
        self.entreeAddresse.grid(row=3, column=0, pady=(5, 10))

        self.confirmationFrame = ctk.CTkFrame(self, height=50)
        self.confirmationFrame.grid(row=1, column=0, sticky="ew", pady=5, padx=5)

        self.valider = ctk.CTkButton(self.confirmationFrame, text="valider", fg_color="green", command=self.verification)
        self.annuler = ctk.CTkButton(self.confirmationFrame, text="annuler", fg_color="red", command=self.fermetureAnormale)
        self.valider.pack(side="right", padx=(5, 5), pady=10)
        self.annuler.pack(side="left", padx=(5, 5), pady=10)

        self.wait_visibility()
        self.grab_set()
        #self.grab_set_global()
        #self.mainloop()

    def verification(self):
        nom = self.entreeNom.get()
        prenom = self.entreePrenom.get()
        telephone = self.entreeTelephone.get()
        addresse = self.entreeAddresse.get().strip()
        #addresse = addresse if re.match(self.emailPattern, addresse) else ""

        if not re.match(self.nomPattern, nom):
            self.rougir(self.entreeNom)
        elif not re.match(self.nomPattern, prenom):
            self.rougir(self.entreePrenom)
        elif not re.match(self.numeroPattern, telephone):
            self.rougir(self.entreeTelephone)
        elif not re.match(self.emailPattern, addresse) and addresse!="":
            self.rougir(self.entreeAddresse)
        else:
            if not self.mode:
                if obtenirClientparAttribue(telephone=telephone): 
                    self.wait_window(erreur(self, "un client possede deja ce numero"))
                elif obtenirClientparAttribue(addresse=addresse) and addresse!="":
                    self.wait_window(erreur(self, "un client possede deja cet addresse"))
                else:
                    self.callback({"nom": nom, "prenom": prenom, "telephone": telephone, "addresse": addresse})
                    self.destroy()
            else:

                for client in obtenirClientparAttribue(telephone=telephone):
                    if (client.id!=self.infoClient["id"]) and (client.telephone==telephone):
                        self.wait_window(erreur(self, "un client possede deja ce numero"))
                        return
                    
                for client in obtenirClientparAttribue(addresse=addresse):
                    if client.id!=self.infoClient["id"] and client.addresse==addresse and addresse!="":
                        self.wait_window(erreur(self, "un client possede deja cet addresse"))
                        return
                    
                self.callback({"nom": nom, "prenom": prenom, "telephone": telephone, "addresse": addresse})
                self.destroy()

    def rougir(self, widget):
        widget.configure(fg_color = "red")
        self.after(1500, lambda:self.blanchir(widget))

    def blanchir(self, widget):
        widget.configure(fg_color="white")


    def fermetureAnormale(self):
        self.callback(None)
        self.destroy()

    def infotaille(self):
        print(f"{self.winfo_width()}, {self.winfo_height()}")