import customtkinter as ctk
import tkinter as tk
from PIL import Image
from .formulaire.categorieFormulaire import categorieForm
from .formulaire.erreur.confirmation import Confirmation
from .formulaire.erreur.erreur import erreur
from controleur.categorieControler import *
from pages.journalisation.log import logs

ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue

class CategoriePage(ctk.CTkFrame):

    categorieAttribue = ("nom", "description")
    rechecheImagePath = "ctkAPP/images/recherche.png"
    reponse = {}
    mode = ""
    autoriserSuppression = False
    listeCategorie = []

    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=1)


        self.titre = ctk.CTkLabel(self, text="categories", font=ctk.CTkFont(family="Arial", size=25, weight="bold"), height=30)
        self.menu = ctk.CTkFrame(self, height=150)
        self.tabFrame = ctk.CTkFrame(self)
        
        self.titre.grid(row=0, column=0)
        self.menu.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 5))
        self.tabFrame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(5, 5))

        self.frameGauche = ctk.CTkFrame(self.menu, height=50)
        self.frameGauche.pack(side="left", padx=3, pady=3)

        ctk.CTkButton(self.frameGauche, text="nouveau", height=35, width=50, fg_color="green", command=self.ajouterCategorie).pack(side="left", padx=3, pady=3)
        ctk.CTkButton(self.frameGauche, text="modifier", height=35, width=50, fg_color="#00AA00", command=self.modifierCategorie).pack(side="right", padx=3, pady=3)
        ctk.CTkButton(self.menu, text="supprimer", height=35, width=50, fg_color="red", command=self.supprimerCategorie).pack(side="right", padx=3, pady=3)

        self.tabFrame.grid_columnconfigure(0, weight=1)
        self.tabFrame.grid_rowconfigure(1, weight=1)
        self.tabFrame.grid_rowconfigure(0, weight=0)

        self.barreRecherche = ctk.CTkFrame(self.tabFrame, height=50)

        style = tk.ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 14))  # Augmenter la taille de la police
        style.configure("mystyle.Treeview.Heading", font=("Arial", 16, "bold"))  # Augmenter la taille de la police des titres
        style.configure("mystyle.Treeview", rowheight=30)  # Augmenter la hauteur des lignes

        self.categorieTab = tk.ttk.Treeview(self.tabFrame,style="mystyle.Treeview", columns=self.categorieAttribue, show="headings")

        self.categorieTab.bind("<Configure>", self.ajusterCategorieTab)
        

        for attribue in self.categorieAttribue:
            self.categorieTab.heading(attribue, text=attribue)

        self.barreRecherche.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.categorieTab.grid(row=1, column=0, sticky="nsew")
        self.barreRecherche.grid_columnconfigure(0, weight=1)
        self.boxRecherche = ctk.CTkFrame(self.barreRecherche, width=300, height=50)
        self.boxRecherche.grid(row=0, column=0, pady=2)

        self.selecteur = ctk.CTkComboBox(self.boxRecherche, values=self.categorieAttribue)
        self.selecteur.set(self.categorieAttribue[0])

        ctk.CTkLabel(self.boxRecherche, text="", image=ctk.CTkImage(Image.open(self.rechecheImagePath))).pack(padx=2, pady=2, side="right")

        self.rechercheEntree = ctk.CTkEntry(self.boxRecherche, width=200)
        self.rechercheEntree.pack(padx=2, pady=2, side="right")
        self.rechercheEntree.bind("<KeyRelease>", self.recherche)

        self.selecteur.pack(side="left", padx=2, pady=2)
        self.miseAjour()

    
    def recherche(self, event=None):
        critere = self.selecteur.get()
        texteRechere = self.rechercheEntree.get()
        match critere:
            case "id":
                self.listeCategorie = obtenirCategorieParAttribue (employeId=eval(texteRechere.strip()), tous=False)
            case "nom":
                self.listeCategorie = obtenirCategorieParAttribue (nom=texteRechere, tous=False)
            case "description":
                self.listeCategorie = obtenirCategorieParAttribue (description=texteRechere, tous=False)
        self.categorieTab.delete(*self.categorieTab.get_children())
        for categorie in self.listeCategorie:
            self.categorieTab.insert("", tk.END, values=(categorie.nom, categorie.description))

        


    def ajouterCategorie(self):
        self.mode = "ajout"
        self.wait_window(categorieForm(self.controller, self.avoirInfo,  {}, mode=False))
        if self.reponse:
            if creerCategorie(
                        nom=self.reponse["nom"],
                        description=self.reponse["description"]
                    ):
                nouveau = obtenirCategorieParAttribue (nom=self.reponse["nom"], description=self.reponse["description"], tous=False, categorieId="")
                logs().logCategorie(nouveau[0], self.controller.utilisateurCourant)
                self.categorieTab.insert("", tk.END, iid=nouveau[0].id,values=(self.reponse["nom"], self.reponse["description"]))


    def modifierCategorie(self):
        selection = self.categorieTab.selection()
        if selection:
            attribues = self.categorieTab.item(selection)["values"]
            categorie = { "nom": attribues[0], "description": attribues[1]}
            self.wait_window(categorieForm(self.controller, self.avoirInfo,  categorie, mode=True))
            if self.reponse:
                ancienCategorie = obtenirCategorieParAttribue(categorieId=selection[0])[0]
                if modifierCategorie(categorieId=eval(selection[0]),
                            nom=self.reponse["nom"],
                            description=self.reponse["description"]
                ):
                    self.categorieTab.item(selection, values=(self.reponse["nom"], self.reponse["description"]))
                    nouvelleCategorie = obtenirCategorieParAttribue(categorieId=selection[0])[0]
                    logs().logCategorie(ancienCategorie, self.controller.utilisateurCourant, nouvelleCategorie, mode=2)
        else:
            self.controller.wait_window(erreur(self.controller, "veuillez choisir\nune categorie"))

    def supprimerCategorie(self):
        selection=self.categorieTab.selection()
        if selection:
            categorie = obtenirCategorieParAttribue(categorieId=selection[0])[0]
            message = "cette action supprimera toutes\nles boissons associees"
            self.wait_window(Confirmation(self.controller, message, self.demandeAutorisation))
            if self.autoriserSuppression:
                supprimerCategorie(selection[0])
                self.categorieTab.delete(selection[0])
                logs().logCategorie(categorie, self.controller.utilisateurCourant, mode=3)
                for boisson in categorie.boissons:
                    logs().logBoisson(boisson, self.controller.utilisateurCourant, mode=3)
        else:
            self.controller.wait_window(erreur(self.controller, "veuillez choisir\nune categorie"))

        
    def miseAjour(self):
        if self.grid_info():
            self.controller.title("categorie")
        self.listeCategorie = obtenirCategorieParAttribue(tous=True, categorieId="", description="", nom="")
        self.categorieTab.delete(*self.categorieTab.get_children())
        for categorie in self.listeCategorie:
            self.categorieTab.insert("", tk.END, iid=categorie.id, values=(categorie.nom, categorie.description))

    def avoirInfo(self, information):
        self.reponse = information



    def ajusterCategorieTab(self, event):
        largeur_totale = self.categorieTab.winfo_width()
        # Proportion : 1/3 pour "Nom" et 2/3 pour "Catégorie"
        self.categorieTab.column("nom", width=int(largeur_totale * 1 / 4))
        self.categorieTab.column("description", width=int(largeur_totale * 3 / 4))


    def demandeAutorisation(self, permission):
        self.autoriserSuppression = permission