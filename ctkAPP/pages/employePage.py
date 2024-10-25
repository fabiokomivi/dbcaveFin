import customtkinter as ctk
import tkinter as tk
from PIL import Image
from controleur.employeControler import *
from .formulaire.employeFormulaire import employeForm
from .formulaire.erreur.confirmation import Confirmation
from .formulaire.erreur.erreur import erreur
from pages.journalisation.log import logs
ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue


class EmployePage(ctk.CTkFrame):


    employeAttribue = ("nom", "prenom", "telephone", "addresse")
    rechecheImagePath = "ctkAPP/images/recherche.png"
    reponse = {}
    mode = ""
    listeCategorie = []

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=1)


        self.titre = ctk.CTkLabel(self, text="employes", font=ctk.CTkFont(family="Arial", size=25, weight="bold"), height=30)
        self.menu = ctk.CTkFrame(self, height=150)
        self.tabFrame = ctk.CTkFrame(self)
        
        self.titre.grid(row=0, column=0)
        self.menu.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 5))
        self.tabFrame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(5, 5))

        self.frameGauche = ctk.CTkFrame(self.menu, height=50)
        self.frameGauche.pack(side="left", padx=3, pady=3)

        ctk.CTkButton(self.frameGauche, text="nouveau", fg_color="green", height=35, width=50, command=self.ajouterEmploye)\
        .pack(side="left", padx=3, pady=3)

        ctk.CTkButton(self.frameGauche, text="modifier", fg_color="#00AA00", height=35, width=50, command=self.modifierEmploye)\
        .pack(side="right", padx=3, pady=3)

        ctk.CTkButton(self.menu, text="supprimer", fg_color="red", height=35, width=50, command=self.supprimerEmploye)\
        .pack(side="right", padx=3, pady=3)

        self.tabFrame.grid_columnconfigure(0, weight=1)
        self.tabFrame.grid_rowconfigure(1, weight=1)
        self.tabFrame.grid_rowconfigure(0, weight=0)

        self.barreRecherche = ctk.CTkFrame(self.tabFrame, height=50)

        style = tk.ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 14))  # Augmenter la taille de la police
        style.configure("mystyle.Treeview.Heading", font=("Arial", 16, "bold"))  # Augmenter la taille de la police des titres
        style.configure("mystyle.Treeview", rowheight=30)  # Augmenter la hauteur des lignes


        self.employeTab = tk.ttk.Treeview(self.tabFrame, style="mystyle.Treeview",columns=self.employeAttribue, show="headings")
        

        for attribue in self.employeAttribue:
            self.employeTab.heading(attribue, text=attribue)

        self.barreRecherche.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.employeTab.grid(row=1, column=0, sticky="nsew")
        self.barreRecherche.grid_columnconfigure(0, weight=1)
        self.boxRecherche = ctk.CTkFrame(self.barreRecherche, width=300, height=50)
        self.boxRecherche.grid(row=0, column=0, pady=2)

        self.selecteur = ctk.CTkComboBox(self.boxRecherche, values=self.employeAttribue[0:4])
        self.selecteur.set(self.employeAttribue[0])

        ctk.CTkLabel(self.boxRecherche, text="", image=ctk.CTkImage(Image.open(self.rechecheImagePath))).pack(padx=2, pady=2, side="right")

        self.rechercheEntree = ctk.CTkEntry(self.boxRecherche, width=200)
        self.rechercheEntree.pack(padx=2, pady=2, side="right")
        self.rechercheEntree.bind("<KeyRelease>", self.recherche)

        self.selecteur.pack(side="left", padx=2, pady=2)
        self.miseAjour()


    def ajouterEmploye(self):
        self.mode = "ajout"
        self.wait_window(employeForm(self.controller, self.avoirInfo, None, False))
        if self.reponse:
            creerEmploye(self.controller.utilisateurCourant.id,
                        self.reponse["nom"],
                        self.reponse["prenom"],
                        self.reponse["telephone"],
                        self.reponse["addresse"],
                        self.reponse["mdp"])
            employe = obtenirEmployePar(telephone=self.reponse["telephone"], addresse=self.reponse["addresse"])[0]
            if employe:
                self.employeTab.insert("", tk.END, iid=employe.id, values=(employe.nom, employe.prenom, employe.telephone, employe.addresse, employe.motDePasse))
                logs().logEmploye(employe, self.controller.utilisateurCourant)

    def modifierEmploye(self):
        selection = self.employeTab.selection()
        if selection:
            attribues = self.employeTab.item(selection)["values"]
            employe = {"id":int(selection[0]), "nom": attribues[0], "prenom": attribues[1], "telephone": str(attribues[2]), "addresse": attribues[3]}
            ancienEmploye = obtenirEmployePar(id=selection[0])
            self.wait_window(employeForm(self.controller, self.avoirInfo,  employe, True))
            if self.reponse:
                if modifierEmploye(employeId=eval(selection[0]),
                            nom=self.reponse["nom"],
                            prenom=self.reponse["prenom"],
                            telephone=self.reponse["telephone"],
                            addresse=self.reponse["addresse"],
                ):
                    nouveauEmploye = obtenirEmployePar(id=selection[0])
                    self.employeTab.item(selection, values=(nouveauEmploye.nom, nouveauEmploye.prenom, nouveauEmploye.telephone, nouveauEmploye.addresse))
                    logs().logEmploye(ancienEmploye, self.controller.utilisateurCourant, nouveauEmploye, mode=2)
        else:
            self.controller.wait_window(erreur(self.controller, "veuillez choisir\nun employe"))

    def avoirInfo(self, information):
        self.reponse = information

    def miseAjour(self):
        if self.grid_info():
            self.controller.title("employe")
        employes = obtenirEmploye()
        if employes:
            self.employeTab.delete(*self.employeTab.get_children())
            for employe in employes:
                self.employeTab.insert("", tk.END, iid=employe.id, values=(employe.nom, employe.prenom, str(employe.telephone), employe.addresse))

    def recherche(self, event=None):
        critere = self.selecteur.get()
        texteRechere = self.rechercheEntree.get()
        self.employeTab.delete(*self.employeTab.get_children())
        employes=None
        match critere:
            case "nom":
                employes = obtenirEmployePar(nom=texteRechere)
            case "prenom":
                employes = obtenirEmployePar(prenom=texteRechere)
            case "telephone":
                employes = obtenirEmployePar(telephone=texteRechere)
            case "addresse":
                employes = obtenirEmployePar(addresse=texteRechere)
        for employe in employes:
            self.employeTab.insert("", tk.END, iid=employe.id, values=(employe.nom, employe.prenom, employe.telephone, employe.addresse, employe.motDePasse))

    def supprimerEmploye(self):
        selection=self.employeTab.selection()
        if selection:
            message = "cette action supprimera toutes\nles clients et commandes \nassociees"
            self.wait_window(Confirmation(self.controller, message, self.demandeAutorisation))
            if self.autoriserSuppression:
                employe = obtenirEmployePar(id=selection[0])
                if supprimerEmploye(selection[0]):
                    self.employeTab.delete(selection)
                    logs().logEmploye(employe, self.controller.utilisateurCourant, mode=3)
        else:
            self.controller.wait_window(erreur(self.controller, "veuillez choisir\nun employe"))

    def demandeAutorisation(self, permission):
        self.autoriserSuppression = permission

    