import customtkinter as ctk
from PIL import Image

class BienvenuePage(ctk.CTkFrame):
    vinImage = ctk.CTkImage(Image.open("/home/fabio/Bureau/python/appCTKenv/ctkAPP/images/bienvenue4.png"), size=(800, 450))
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        ctk.CTkLabel(self, text="", width=300, image=self.vinImage).grid(row=0, column=0, sticky="nsew")
        self.controller= controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def miseAjour(self):
        if self.grid_info():
            self.controller.title("bienvenu")



