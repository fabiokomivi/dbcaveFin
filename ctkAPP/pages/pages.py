import customtkinter as ctk

class Record(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Créer le conteneur pour centrer les éléments
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, padx=100, pady=50, sticky="nsew")

        # Champs de texte
        self.entryIne = self.create_entry(self.container, "Entrer votre INE", 1)
        self.entryNom = self.create_entry(self.container, "Entrer votre nom", 2)
        self.entryPrenom = self.create_entry(self.container, "Entrer votre prénom", 3)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_entry(self, parent, placeholder, row):
        """Crée un champ d'entrée générique."""
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.grid(row=row, column=0, padx=10, pady=10)
        return entry

class DashBoard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Label
        label = ctk.CTkLabel(self, text="Tableau de bord")
        label.grid(row=0, column=0, padx=100, pady=100, sticky="ew")

        # Champs de texte
        self.entryIne = self.create_entry(self, "Entrer votre INE", 1)
        self.entryNom = self.create_entry(self, "Entrer votre nom", 2)
        self.entryPrenom = self.create_entry(self, "Entrer votre prénom", 3)

    def create_entry(self, parent, placeholder, row):
        """Crée un champ d'entrée générique."""
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.grid(row=row, column=0, padx=10, pady=10)
        return entry
    
class Commande(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
