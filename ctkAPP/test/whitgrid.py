import customtkinter as ctk

# Initialiser CustomTkinter
ctk.set_appearance_mode("dark")  # Mode clair
ctk.set_default_color_theme("blue")  # Thème bleu

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Interface avec Menu et Contenu")
        self.geometry("800x400")

        # Créer un cadre pour le menu (à gauche)
        self.menu_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="lightgray")
        self.menu_frame.grid(row=0, column=0, sticky="ns")  # Fixe le cadre à gauche

        # Créer un cadre pour le contenu (à droite)
        self.content_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="lightblue")
        self.content_frame.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")  # Remplit le reste de l'espace

        # Configurer la grille pour que le contenu prenne tout l'espace disponible
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Permet au cadre de contenu de s'étendre verticalement

        # Ajouter des widgets au menu
        """menu_label = ctk.CTkLabel(self.menu_frame, text="Menu", font=("Arial", 20))
        menu_label.grid(row=0, column=0, pady=20)

        menu_button1 = ctk.CTkButton(self.menu_frame, text="Option 1")
        menu_button1.grid(row=1, column=0, pady=10)

        menu_button2 = ctk.CTkButton(self.menu_frame, text="Option 2")
        menu_button2.grid(row=2, column=0, pady=10)

        # Ajouter des widgets au contenu
        content_label = ctk.CTkLabel(self.content_frame, text="Contenu", font=("Arial", 24))
        content_label.grid(row=0, column=0, pady=20)
        """
if __name__ == "__main__":
    app = App()
    app.mainloop()

"""import customtkinter as ctk

# Initialisation de l'interface
app = ctk.CTk()
app.title("Hostel Management System")
app.geometry("800x500")

# Configuration de l'apparence
ctk.set_appearance_mode("light")  # Mode clair
ctk.set_default_color_theme("green")  # Thème couleur verte

# Cadre pour la barre latérale
sidebar = ctk.CTkFrame(app, width=200, height=500, corner_radius=0)
sidebar.grid(row=0, column=0, sticky="nswe")

# Titre dans la barre latérale
title_label = ctk.CTkLabel(sidebar, text="Hostel", font=ctk.CTkFont(size=20, weight="bold"))
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

subtitle_label = ctk.CTkLabel(sidebar, text="Management System", font=ctk.CTkFont(size=12))
subtitle_label.grid(row=1, column=0, padx=10, pady=0, sticky="w")

# Options de menu
menu_options = ["Dashboard", "Students", "Employees", "Hostels", "Rooms"]
for i, option in enumerate(menu_options, start=2):
    menu_button = ctk.CTkButton(sidebar, text=option, width=180)
    menu_button.grid(row=i, column=0, padx=10, pady=10, sticky="w")

# Cadre principal pour le contenu du tableau de bord
dashboard_frame = ctk.CTkFrame(app, width=600, height=500)
dashboard_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

# Titre du tableau de bord
dashboard_title = ctk.CTkLabel(dashboard_frame, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
dashboard_title.grid(row=0, column=0, padx=10, pady=10)

# Cadre pour les cartes de statistiques
cards_frame = ctk.CTkFrame(dashboard_frame)
cards_frame.grid(row=1, column=0, padx=10, pady=20)

# Création des cartes de statistiques
stats = [("Total Munshi", "2"), ("Total Servants", "20"), ("Total Students", "450")]
for i, (label_text, value) in enumerate(stats):
    card = ctk.CTkFrame(cards_frame, width=150, height=150, corner_radius=15)
    card.grid(row=0, column=i, padx=20)

    label = ctk.CTkLabel(card, text=label_text, font=ctk.CTkFont(size=16))
    label.pack(pady=10)

    value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"))
    value_label.pack()

# Démarrer l'application
app.mainloop()"""