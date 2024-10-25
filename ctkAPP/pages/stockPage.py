import customtkinter as ctk
import tkinter as tk
from PIL import Image
from controleur.stockControler import *
from controleur.boissonControler import *
from .formulaire.stockFormulaire import stockForm
from .formulaire.erreur.erreur import erreur
from pages.journalisation.log import logs
import re
ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue
class StockPage(ctk.CTkFrame):


    stockAttribue = ("nom", "quantite")
    rechecheImagePath = "ctkAPP/images/recherche.png"
    reponse = {}
    mode = ""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=1)


        self.titre = ctk.CTkLabel(self, text="stock", font=ctk.CTkFont(family="Arial", size=25, weight="bold"), height=30)
        self.menu = ctk.CTkFrame(self, height=150)
        self.tabFrame = ctk.CTkFrame(self)
        
        self.titre.grid(row=0, column=0)
        self.menu.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 5))
        self.tabFrame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(5, 5))

        self.nouveauBoutton = ctk.CTkButton(self.menu, text="ajouter", command=self.ajouter, height=35, fg_color="green")
        self.nouveauBoutton.pack(side="right", padx=10, pady=3)

        self.tabFrame.grid_columnconfigure(0, weight=1)
        self.tabFrame.grid_rowconfigure(1, weight=1)
        self.tabFrame.grid_rowconfigure(0, weight=0)

        self.barreRecherche = ctk.CTkFrame(self.tabFrame, height=50)

        style = tk.ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 14))  # Augmenter la taille de la police
        style.configure("mystyle.Treeview.Heading", font=("Arial", 16, "bold"))  # Augmenter la taille de la police des titres
        style.configure("mystyle.Treeview", rowheight=30)  # Augmenter la hauteur des lignes
        self.stockTab = tk.ttk.Treeview(self.tabFrame, style="mystyle.Treeview", columns=self.stockAttribue, show="headings")
        

        for attribue in self.stockAttribue:
            self.stockTab.heading(attribue, text=attribue)

        self.barreRecherche.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.stockTab.grid(row=1, column=0, sticky="nsew")
        self.barreRecherche.grid_columnconfigure(0, weight=1)
        self.boxRecherche = ctk.CTkFrame(self.barreRecherche, width=300, height=50)
        self.boxRecherche.grid(row=0, column=0, pady=2)

        self.selecteur = ctk.CTkComboBox(self.boxRecherche, values=self.stockAttribue)
        self.selecteur.set(self.stockAttribue[0])

        ctk.CTkLabel(self.boxRecherche, text="", image=ctk.CTkImage(Image.open(self.rechecheImagePath))).pack(padx=2, pady=2, side="right")

        self.rechercheEntree = ctk.CTkEntry(self.boxRecherche, width=200)
        self.rechercheEntree.pack(padx=2, pady=2, side="right")
        self.rechercheEntree.bind("<KeyRelease>", self.recherche)

        self.selecteur.pack(side="left", padx=2, pady=2)
        self.miseAjour()

    def miseAjour(self):
        if self.grid_info():
            self.controller.title("stock")
        stocks = obtenirStock()
        self.stockTab.delete(*self.stockTab.get_children())
        for stock in stocks:
            boisson = obtenirBoissonParAttribue(boissonId=stock.boissonId)
            self.stockTab.insert("", tk.END, iid=stock.id, values=(boisson.nom, stock.quantite))

    def ajouter(self):
        selection = self.stockTab.selection()
        if selection:
            stock = obtenirStockPar(stockId=selection[0])
            boisson = obtenirBoissonParAttribue(boissonId=stock.boissonId)
            self.wait_window(stockForm(self.controller, self.avoirInfo, boisson.nom))
            if self.reponse:
                if ajouterStock(stock.id, self.reponse):
                    stock = obtenirStockPar(stockId=selection[0])
                    self.stockTab.item(selection[0], values=(boisson.nom, stock.quantite))
                    logs().logStock(boisson, self.reponse, stock.quantite)
        else:
            self.controller.wait_window(erreur(self.controller, "veuillez choisir\nune boisson"))

    def recherche(self, event=None):
        critere = self.selecteur.get()
        texteRechere = self.rechercheEntree.get()
        match critere:
            case "nom":
                boissons = obtenirBoissonParAttribue(nom=texteRechere)
                self.stockTab.delete(*self.stockTab.get_children())
                for boisson in boissons:
                    self.stockTab.insert("", tk.END, iid=boisson.stock.id, values=(boisson.nom, boisson.stock.quantite))
            case "quantite":
                if re.match(r"[0-9]+", texteRechere):
                    stocks = obtenirStockPar(quantite=int(texteRechere))
                    self.stockTab.delete(*self.stockTab.get_children())
                    for stock in stocks:
                        boisson = obtenirBoissonParAttribue(boissonId=stock.boissonId)
                        self.stockTab.insert("", tk.END, iid=stock.id, values=(boisson.nom, stock.quantite))
                else:
                    self.miseAjour()

    def avoirInfo(self, information):
        self.reponse=information

    