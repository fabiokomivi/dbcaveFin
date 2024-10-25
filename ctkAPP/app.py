import time
import customtkinter as ctk
from widget.widget import menuItem
from pages.commandePage import CommandePage
from pages.clientPage import ClientPage
from pages.parametrePage import ParametrePage
from pages.parametreGerantPage import ParametreGerantPage
from pages.gestionPage import GestionPage
from pages.categoriePage import CategoriePage
from pages.boissonPage import BoissonPage
from pages.employePage import EmployePage
from pages.stockPage import StockPage
from pages.dashboardPage import DashboardPage
from pages.formulaire.premiereConnexion import PremiereConnexion
from controleur.chefControler import *

from pages.bienvenue import BienvenuePage
from pages.connexionPage import ConnexionPage
from pages.contentPage import ContentPage
from PIL import Image 

from controleur.chefControler import *
from controleur.employeControler import *

from pages.journalisation.log import logs
from models.database import fermerTout, init_db
import gc
import matplotlib.pyplot as plt

# Initialiser CustomTkinter
ctk.set_appearance_mode("light")  # Mode sombre
ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue


class APP(ctk.CTk):

    commandImagePath = "ctkAPP/images/commande.png"
    clientImagePath = "ctkAPP/images/client.png"
    bossImagePath = "ctkAPP/images/boss.png"
    dashboardImagePath = "ctkAPP/images/dashboard.png"
    deleteImagePath = "ctkAPP/images/delete.png"
    exitImagePath = "ctkAPP/images/exit.png"
    settingImagePath = "ctkAPP/images/settings.png"
    employeImagePath = "ctkAPP/images/employe.png"
    boissonImagePath = "ctkAPP/images/bouteille.png"
    chefImagePath = "ctkAPP/images/chef.png"
    stockImagePath = "ctkAPP/images/stock.png"
    categorieImagePath = "ctkAPP/images/categorie.png"

    pagesPrimaire = {}
    pagesSecondaire = {}
    pagesEmploye = {}
    pagesChef = {}

    utilisateurType = ""
    utilisateurCourant = None
    chef = {}



    def __init__(self):
        super().__init__()

        self.geometry("1200x650")
        self.minsize(1100, 650)
        self.title("bienvenu")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # creation du conteneur supreme
        self.root=ctk.CTkFrame(self)  #creation de la fenetre root
        self.root.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # chargement des differentes pages
        self.chargerPagePrimaire()
        self.chargerPageSecondaire()
        self.chargerPageEmploye()
        self.chargerPageGestion()
        self.protocol("WM_DELETE_WINDOW", self.deconnexion)

        self.estPremiereConnexion()
        self.after(100, self.remplaceBienvenue)
        self.mainloop()
    
    def chargerPagePrimaire(self):
        self.pagesPrimaire["bienvenue"] = BienvenuePage(self.root, self)
        self.pagesPrimaire["connexion"] = ConnexionPage(self.root, self)
        self.pagesPrimaire["contenu"] = ContentPage(self.root, self)

        for pagePrimaire in self.pagesPrimaire.values():
            pagePrimaire.grid(row=0, column=0, sticky="nsew")

        self.pagesPrimaire["bienvenue"].miseAjour()
        self.pagesPrimaire["bienvenue"].tkraise()

        
    def chargerPageSecondaire(self):
        self.pagesSecondaire["pageEmploye"] = ctk.CTkFrame(self.pagesPrimaire["contenu"])
        self.pagesSecondaire["gestions"] = ctk.CTkFrame(self.pagesPrimaire["contenu"])

        for pageSecondaire in self.pagesSecondaire.values():
            pageSecondaire.grid_columnconfigure(0, weight=0)
            pageSecondaire.grid_columnconfigure(1, weight=1)
            pageSecondaire.grid_rowconfigure(0, weight=1)

            pageSecondaire.grid(row=0, column=0, columnspan=2, sticky="nsew")


    def chargerPageEmploye(self):
        self.chargerMenuEmploye()
        self.employeContenu=ctk.CTkFrame(self.pagesSecondaire["pageEmploye"])
        self.employeContenu.grid(row=0, column=1, sticky="nsew")
        self.employeContenu.grid_columnconfigure(0, weight=1)
        self.employeContenu.grid_rowconfigure(0, weight=1)

        self.pagesEmploye["clients"] = ClientPage(self.employeContenu, self)
        self.pagesEmploye["commandes"] = CommandePage(self.employeContenu, self)
        self.pagesEmploye["parametres"] = ParametrePage(self.employeContenu, self)
        for pageEmploye in self.pagesEmploye.values():
            pageEmploye.grid(row=0, column=0, sticky="nsew",padx=(5, 7), pady=7)
        self.pagesEmploye["clients"].tkraise()


    def chargerPageGestion(self):
        self.chargerMenuGestion()
        self.chefContenu=ctk.CTkFrame(self.pagesSecondaire["gestions"])
        self.chefContenu.grid_columnconfigure(0, weight=1)
        self.chefContenu.grid_rowconfigure(0, weight=1)
        self.chefContenu.grid(row=0, column=1, sticky="nsew")

        self.pagesChef["boissons"] = BoissonPage(self.chefContenu, self)
        self.pagesChef["categories"] = CategoriePage(self.chefContenu, self)
        self.pagesChef["employes"] = EmployePage(self.chefContenu, self)
        self.pagesChef["stock"] = StockPage(self.chefContenu, self)
        self.pagesChef["parametre"] = ParametreGerantPage(self.chefContenu, self)
        self.pagesChef["dashboard"] = DashboardPage(self.chefContenu, self)
        for gestions in self.pagesChef.values():
            gestions.grid(row=0, column=0, sticky="nsew")

        self.pagesChef["dashboard"].tkraise()

    def chargerMenuEmploye(self):
        self.menuEmploye = ctk.CTkFrame(self.pagesSecondaire["pageEmploye"], width=200)
        self.menuEmploye.grid_columnconfigure(0, weight=1)
        self.menuEmploye.grid_propagate(False)
        self.menuEmploye.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(self.menuEmploye, text="menu", font=ctk.CTkFont(family="Arial", size=25, weight="bold"))\
            .pack(pady=(10, 15))
        menuItem(self.menuEmploye, self, "clients", self.clientImagePath)\
            .pack(padx=3, pady=3, fill="x")
        menuItem(self.menuEmploye, self, "commandes", self.commandImagePath)\
            .pack(padx=3,pady=3, fill="x")
        menuItem(self.menuEmploye, self, "parametres", self.settingImagePath)\
            .pack(padx=3,pady=3, fill="x")
        menuItem(self.menuEmploye, self, "deconnexion", self.exitImagePath)\
            .pack(padx=3, pady=3, side="bottom", fill="x")

    def chargerMenuGestion(self):
        self.menuChef = ctk.CTkFrame(self.pagesSecondaire["gestions"], width=200)
        self.menuChef.grid_columnconfigure(0, weight=1)
        self.menuChef.grid_propagate(False)
        self.menuChef.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(self.menuChef, text="menu", font=ctk.CTkFont(family="Arial", size=25, weight="bold"))\
            .pack(pady=(10, 15))
        menuItem(self.menuChef, self, "dashboard", self.dashboardImagePath)\
            .pack(side="top", padx=5, pady=3, fill="x")
        menuItem(self.menuChef, self, "categories", self.categorieImagePath)\
            .pack(side="top", padx=5, pady=3, fill="x")
        menuItem(self.menuChef, self, "boissons", self.boissonImagePath)\
            .pack(side="top", padx=5, pady=3, fill="x")
        menuItem(self.menuChef, self, "stock", self.stockImagePath)\
            .pack(side="top", padx=5, pady=3, fill="x")
        menuItem(self.menuChef, self, "employes", self.employeImagePath)\
            .pack(side="top", padx=5, pady=3, fill="x")
        menuItem(self.menuChef, self, "parametre", self.settingImagePath)\
            .pack(side="top", padx=5, pady=3, fill="x")
        menuItem(self.menuChef, self, "deconnexion", self.exitImagePath)\
            .pack(side="bottom", padx=5, pady=3, fill="x")
        


    def setTheme(self):
        # Basculer entre les modes clair et sombre
        current_mode = ctk.get_appearance_mode()
        
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")



    def initPages(self):
        self.pages["commandes"] = CommandePage(self.contentEmploye, self)
        self.pages["clients"] = ClientPage(self.contentEmploye, self)
        self.pages["parametres"] = ParametrePage(self.contentEmploye, self)
        self.pages["gestions"] = GestionPage(self.contentEmploye, self)

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")
        self.pages["commandes"].tkraise()
        


    def loadImage(self, imagePath, size):
        return ctk.CTkImage(Image.open(imagePath), size=size)
    
    def changePage(self, pageName):
        if pageName == "deconnexion":
            self.pagesPrimaire["connexion"].miseAjour()
            self.pagesPrimaire["connexion"].tkraise()
            logs().logConnexion(self.utilisateurCourant, mode=2)
            self.utilisateurCourant=None
            self.utilisateurType=None

        elif pageName in self.pagesPrimaire.keys():
            self.pagesPrimaire["connexion"].miseAjour()
            self.pagesPrimaire["connexion"].tkraise()


        elif pageName in self.pagesSecondaire.keys():
            self.pagesSecondaire[pageName].tkraise()
            self.title("")

        elif pageName in self.pagesEmploye.keys():
            self.pagesEmploye[pageName].miseAjour()
            self.pagesEmploye[pageName].tkraise()


        elif pageName in self.pagesChef.keys():
            self.pagesChef[pageName].miseAjour()
            self.pagesChef[pageName].tkraise()


    def remplaceBienvenue(self):
        self.changePage("connexion")

    def estPremiereConnexion(self):
        if not obtenirChefs():
            self.wait_window(PremiereConnexion(self, self.avoirInfo))
            if self.chef:
                creerChef(*self.chef.values())
            else:
                self.destroy()

    def avoirInfo(self, chef):
        self.chef = chef

    def deconnexion(self):
        if self.utilisateurCourant:
            logs().logConnexion(self.utilisateurCourant, mode=2)
        plt.close('all')
        self.destroy()
        gc.collect()


# Lancer l'application
init_db()
try:
    APP()
except:
    ...
finally:
    fermerTout()
