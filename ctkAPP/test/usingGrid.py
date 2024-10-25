#import tkinter as tk
#
#root = tk.Tk()
#root.title("Exemple de Grid")
#
## Créer des étiquettes et des boutons
#label1 = tk.Label(root, text="Étiquette 1")
#label2 = tk.Label(root, text="Étiquette 2")
#button1 = tk.Button(root, text="Bouton 1")
#button2 = tk.Button(root, text="Bouton 2")
#
#button3 = tk.Button(root, text="Bouton 3")
#
## Placer les widgets avec grid()
#label1.grid(row=0, column=0, padx=10, pady=10)
#label2.grid(row=0, column=1, padx=10, pady=10)
#button1.grid(row=1, column=0, padx=100, pady=100, sticky="ew")
#button2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
#button3.grid(row=1, column=2, rowspan=3, columnspan=2, padx=10, pady=10, sticky="nsew")
#
#
## Configurer les colonnes pour s'étendre
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=1)
#root.grid_columnconfigure(2, weight=1)
#root.grid_rowconfigure(1, weight=1)
#
#root.mainloop()
import customtkinter as ctk

# Initialiser CustomTkinter
ctk.set_appearance_mode("light")  # Mode clair
ctk.set_default_color_theme("blue")  # Thème bleu

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Interface avec Menu et Contenu")
        self.geometry("800x400")

        # Créer un cadre pour le menu (à gauche)
        self.menu_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="blue")
        self.menu_frame.pack(side="left", fill="y")

        # Créer un cadre pour le contenu (à droite)
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="red")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Ajouter des widgets au menu
        menu_label = ctk.CTkLabel(self.menu_frame, text="Menu", font=("Arial", 20))
        menu_label.pack(pady=20)

        menu_button1 = ctk.CTkButton(self.menu_frame, text="Option 1")
        menu_button1.pack(pady=10)

        menu_button2 = ctk.CTkButton(self.menu_frame, text="Option 2")
        menu_button2.pack(pady=10)

        # Ajouter des widgets au contenu
        content_label = ctk.CTkLabel(self.content_frame, text="Contenu", font=("Arial", 24))
        content_label.pack(pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()
