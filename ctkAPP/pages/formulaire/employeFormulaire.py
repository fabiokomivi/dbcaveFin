import customtkinter as ctk
import re
from .erreur.erreur import erreur
from controleur.employeControler import *
import tkinter as tk




class employeForm(ctk.CTkToplevel):

    emailPattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    numeroPattern = r"[0-9]{8}"
    nomPattern = r"[a-zA-Z]"
    mpdPattern = r"[a-zA-Z0-9@$!%*?&]+"

    def __init__(self, parent, callback, infoEmploye, mode=False):
        super().__init__(parent)
        self.protocol("WM_DELETE_WINDOW", self.fermetureAnormale)
        self.attributes('-topmost', True)
        self.geometry("316x243")
        self.resizable(False, False)
        self.centreFenetre()
        self.callback = callback
        self.infoEmploye = infoEmploye
        self.mode = mode
        self.title("ajout employe" if not self.mode else "modification employe")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.contenu = ctk.CTkFrame(self)
        self.contenu.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.initTop()
        self.wait_visibility()
        self.grab_set()

    def initTop(self):
        self.contenu.grid_rowconfigure(0, weight=1)
        self.contenu.grid_rowconfigure(1, minsize=25)
        self.contenu.grid_columnconfigure(0, weight=1)

        topFrame = ctk.CTkFrame(self.contenu)
        bottomFrame = ctk.CTkFrame(self.contenu, height=50)

        topFrame.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
        bottomFrame.grid(row=1, column=0, sticky="ew", padx=3, pady=3)

        ctk.CTkButton(bottomFrame, text="annuler", fg_color="red", command=self.fermetureAnormale).pack(side="left", padx=5, pady=3)
        ctk.CTkButton(bottomFrame, text="valider", fg_color="green", command=self.verification).pack(side="right", padx=5, pady=3)

        self.entreeNom = ctk.CTkEntry(topFrame, placeholder_text="nom")
        self.entreePrenom = ctk.CTkEntry(topFrame, placeholder_text="prenom")
        self.entreeTelephone = ctk.CTkEntry(topFrame, placeholder_text="telephone")
        self.entreeAddresse = ctk.CTkEntry(topFrame, placeholder_text="addresse")
        self.entreeMDP = ctk.CTkEntry(topFrame, placeholder_text="mot de passe")

        if self.infoEmploye:
            self.entreeNom.insert(0, self.infoEmploye["nom"])
            self.entreePrenom.insert(0, self.infoEmploye["prenom"])
            self.entreeTelephone.insert(0, self.infoEmploye["telephone"])
            self.entreeAddresse.insert(0, self.infoEmploye["addresse"])
            self.entreeMDP.configure(state=tk.DISABLED)
        self.entreeNom.pack(side="top", padx=10, pady=3, fill="x")
        self.entreePrenom.pack(side="top", padx=10, pady=3, fill="x")
        self.entreeTelephone.pack(side="top", padx=10, pady=3, fill="x")
        self.entreeAddresse.pack(side="top", padx=10, pady=3, fill="x")
        self.entreeMDP.pack(side="top", padx=10, pady=3, fill="x")

    def verification(self):
        nom = self.entreeNom.get()
        prenom = self.entreePrenom.get()
        telephone = self.entreeTelephone.get()
        addresse = self.entreeAddresse.get()
        mdp = self.entreeMDP.get()

        if not re.match(self.nomPattern, nom):
            self.rougir(self.entreeNom)
        elif not re.match(self.nomPattern, prenom):
            self.rougir(self.entreePrenom)
        elif not re.match(self.numeroPattern, telephone):
            self.rougir(self.entreeTelephone)
        elif not re.match(self.emailPattern, addresse):
            self.rougir(self.entreeAddresse)
        elif not re.match(self.mpdPattern, mdp) and not self.mode:
            self.rougir(self.entreeMDP)
        else:
            if not self.mode:
                if obtenirEmployePar(telephone=telephone): 
                    self.wait_window(erreur(self, "un employe possede deja ce numero"))
                elif obtenirEmployePar(addresse=addresse):
                    self.wait_window(erreur(self, "un employe possede deja cet addresse"))
                else:
                    self.callback({"nom": nom, "prenom": prenom, "telephone": telephone, "addresse": addresse, "mdp": mdp})
                    self.destroy()
            else :
                for employe in obtenirEmployePar(telephone=telephone):
                    if (employe.id!=self.infoEmploye["id"]) and (employe.telephone==telephone):
                        self.wait_window(erreur(self, "un employe possede deja ce numero"))
                        return
                    
                for employe in obtenirEmployePar(addresse=addresse):
                    if employe.id!=self.infoEmploye["id"] and employe.addresse==addresse:
                        self.wait_window(erreur(self, "un employe possede deja cet addresse"))
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

    def hasher(self, password):
        passwordBytes = password.encode('utf-8')
        passwordHash = hashlib.sha256(passwordBytes)
        return passwordHash.hexdigest()