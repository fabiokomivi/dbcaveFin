import customtkinter as ctk
import tkinter as tk

class ScrollableFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Créer un Canvas qui servira de zone de scroll
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Ajouter une Scrollbar verticale
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configurer le canvas pour utiliser la scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Créer un frame à l'intérieur du canvas, qui contiendra les widgets scrollables
        self.scrollable_frame = ctk.CTkFrame(self.canvas, bg="lightgray")

        # Créer une fenêtre dans le canvas qui contient le frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configurer la mise à jour de la taille du frame
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event=None):
        """Met à jour la zone scrollable selon la taille du frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# Exemple d'utilisation

app = ctk.CTk()

# Créer un frame scrollable
scrollable_frame = ScrollableFrame(app)
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Ajouter des widgets dans le frame scrollable
for i in range(20):
    button = ctk.CTkButton(scrollable_frame.scrollable_frame, text=f"Button {i+1}")
    button.pack(pady=5)

# Lancer l'application
app.mainloop()
