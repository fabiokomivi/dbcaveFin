import customtkinter as ctk
ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue
from PIL import Image

class myButton(ctk.CTkButton):
    def __init__(self, parent, controller, text):
        super().__init__(parent, text=text, width=70, command= lambda:controller.changePage(text) )
        self.change(text)
    def change(self, text):
        if text=="deconnexion":
            self.configure(fg_color="red")

class menuItem(ctk.CTkFrame):
    def __init__(self, parent, controller, buttonText, image_path):
        super().__init__(parent, height=100)
        self.controller = controller

        # Charger l'image avec PIL
        image = Image.open(image_path)

        # Créer un CTkImage à partir de l'image PIL pour permettre la mise à l'échelle sur HighDPI
        ctk_image = ctk.CTkImage(light_image=image, size=(45, 45))

        # Ajouter un label avec l'image CTkImage
        ctk.CTkLabel(self, text="", image=ctk_image, width=45, height=45).grid(row=0, column=0, padx=5, pady=5)

        # Ajouter le bouton
        myButton(self, controller, buttonText).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Configurer le layout
        self.columnconfigure(0, weight=0)  # La colonne avec l'image
        self.columnconfigure(1, weight=1)  # La colonne avec le bouton (expand)
        self.rowconfigure(0, weight=1, minsize=75)  # Laisser assez de hauteur

        # Placer le frame dans le grid layout

        # Sauvegarder l'image pour éviter qu'elle soit garbage collectée
        self.ctk_image = ctk_image