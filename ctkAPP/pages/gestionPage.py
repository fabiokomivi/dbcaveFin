import customtkinter as ctk
ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue

class GestionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        #test
        ctk.CTkLabel(self, text="super user").grid(row=0, column=0)
