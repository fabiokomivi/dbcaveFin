import customtkinter as ctk
from PIL import Image

# Initialiser CustomTkinter
ctk.set_appearance_mode("dark")  # Mode sombre
ctk.set_default_color_theme("blue")  # Thème bleu

class App(ctk.CTk):

    
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("Navigation avec CustomTkinter")
        self.geometry("600x400")

        # Créer un conteneur pour les frames/pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionnaire pour stocker les frames/pages
        self.frames = {}

        # Initialisation des différentes pages
        for F in (Page1, Page2, Page3):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Afficher la première page
        self.show_frame("Page1")

    def show_frame(self, page_name):
        """Afficher la frame/page demandée."""
        frame = self.frames[page_name]
        frame.tkraise()  # Mettre la frame au premier plan


class Page1(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Contenu de la Page 1
        label = ctk.CTkLabel(self, text="Page 1", font=("Arial", 24))
        label.pack(pady=10)

        # Boutons de navigation
        button_next = ctk.CTkButton(self, text="Aller à la Page 2", command=lambda: controller.show_frame("Page2"))
        button_next.pack()

        button_quit = ctk.CTkButton(self, text="Quitter", command=self.quit)
        button_quit.pack()


class Page2(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Contenu de la Page 2
        label = ctk.CTkLabel(self, text="Page 2", font=("Arial", 24))
        label.pack(pady=10)

        # Boutons de navigation
        button_prev = ctk.CTkButton(self, text="Retour à la Page 1", command=lambda: controller.show_frame("Page1"))
        button_prev.pack()

        button_next = ctk.CTkButton(self, text="Aller à la Page 3", command=lambda: controller.show_frame("Page3"))
        button_next.pack()


class Page3(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Contenu de la Page 3
        label = ctk.CTkLabel(self, text="Page 3", font=("Arial", 24))
        label.pack(pady=10)

        # Boutons de navigation
        button_prev = ctk.CTkButton(self, text="Retour à la Page 2", command=lambda: controller.show_frame("Page2"))
        button_prev.pack()

        button_quit = ctk.CTkButton(self, text="Quitter", command=self.quit)
        button_quit.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
