import customtkinter as ctk
ctk.set_default_color_theme("ctkAPP/themes/myBlue.json")  # Thème bleue

class ContentPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

