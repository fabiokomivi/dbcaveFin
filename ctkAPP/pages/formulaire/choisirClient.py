import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from controleur.clientControler import *
from .erreur.erreur import erreur
from PIL import Image
import re

class choixClient(ctk.CTkToplevel):

    clientAttribue = ("nom", "prenom", "telephone", "addresse")
    rechecheImagePath = "/home/fabio/Bureau/python/appCTKenv/ctkAPP/images/recherche.png"
    reponse = {}
    mode = ""
    listeClient = []

    def __init__(self, parent, commande):
        super().__init__(parent)
        self.commandeTmp = commande
        self.protocol("WM_DELETE_WINDOW", self.annuler)
        self.attributes('-topmost', True)
        self.geometry("800x450")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        contenu = ctk.CTkFrame(self)
        contenu.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        contenu.grid_columnconfigure(0, weight=1)
        contenu.grid_rowconfigure(0, weight=0)
        contenu.grid_rowconfigure(0, weight=0)
        contenu.grid_rowconfigure(2, weight=1)


        self.titre = ctk.CTkLabel(contenu, text="clients", font=ctk.CTkFont(family="Arial", size=25, weight="bold"), height=30)
        self.menu = ctk.CTkFrame(contenu, height=150)
        self.tabFrame = ctk.CTkFrame(contenu)
        
        self.titre.grid(row=0, column=0)
        self.menu.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 5))
        self.tabFrame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(5, 5))

        

        ctk.CTkButton(self.menu, fg_color="green", text="selectionner", height=35, width=50, command=self.valider).pack(side="right", padx=3, pady=3)
        ctk.CTkButton(self.menu, fg_color="red", text="annuler", height=35, width=50, command=self.annuler).pack(side="left", padx=3, pady=3)



        self.tabFrame.grid_columnconfigure(0, weight=1)
        self.tabFrame.grid_rowconfigure(1, weight=1)
        self.tabFrame.grid_rowconfigure(0, weight=0)

        self.barreRecherche = ctk.CTkFrame(self.tabFrame, height=50)

        style = tk.ttk.Style()
        style.configure("mystyle.Treeview", font=("Arial", 14))  # Augmenter la taille de la police
        style.configure("mystyle.Treeview.Heading", font=("Arial", 16, "bold"))  # Augmenter la taille de la police des titres
        style.configure("mystyle.Treeview", rowheight=30)  # Augmenter la hauteur des lignes
        self.clientTab = tk.ttk.Treeview(self.tabFrame, style="mystyle.Treeview", columns=self.clientAttribue, show="headings")
        

        for attribue in self.clientAttribue:
            self.clientTab.heading(attribue, text=attribue)

        self.barreRecherche.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.clientTab.grid(row=1, column=0, sticky="nsew")
        self.barreRecherche.grid_columnconfigure(0, weight=1)
        self.boxRecherche = ctk.CTkFrame(self.barreRecherche, width=300, height=50)
        self.boxRecherche.grid(row=0, column=0, pady=2)

        self.selecteur = ctk.CTkComboBox(self.boxRecherche, values=self.clientAttribue)
        self.selecteur.set(self.clientAttribue[0])

        ctk.CTkLabel(self.boxRecherche, text="", image=ctk.CTkImage(Image.open(self.rechecheImagePath))).pack(padx=2, pady=2, side="right")

        self.rechercheEntree = ctk.CTkEntry(self.boxRecherche, width=200)
        self.rechercheEntree.pack(padx=2, pady=2, side="right")
        self.rechercheEntree.bind("<KeyRelease>", self.recherche)

        self.selecteur.pack(side="left", padx=2, pady=2)
        self.miseAJourTable()

        self.wait_visibility()
        self.grab_set()

    def recherche(self, event=None):
        critere = self.selecteur.get()
        texteRechere = self.rechercheEntree.get()
        self.clientTab.delete(*self.clientTab.get_children())
        match critere:
            case "id":
                self.listeClient = obtenirClientparAttribue(employeId=eval(texteRechere.strip()))
            case "nom":
                self.listeClient = obtenirClientparAttribue(nom=texteRechere)
            case "prenom":
                self.listeClient = obtenirClientparAttribue(prenom=texteRechere)
            case "telephone":
                self.listeClient = obtenirClientparAttribue(telephone=texteRechere)
            case "addresse":
                self.listeClient = obtenirClientparAttribue(addresse=texteRechere)
        for client in self.listeClient:
            self.clientTab.insert("", tk.END, values=(client.nom, client.prenom, client.telephone, client.addresse))

    def miseAJourTable(self):
        self.listeClient = obtenirClients()
        self.clientTab.delete(*self.clientTab.get_children())
        for client in self.listeClient:
            self.clientTab.insert("", tk.END, iid=client.id, values=(client.nom, client.prenom, client.telephone, client.addresse))

    def valider(self):
        selection = self.clientTab.selection()
        if selection:
            client = obtenirClientparAttribue(clientId=selection[0])
            self.commandeTmp.clientId=client.id
            self.destroy()
        
    def annuler(self):
        self.destroy()


