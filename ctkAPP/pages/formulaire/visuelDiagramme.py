import customtkinter as ctk
from PIL import Image


class DiagramViewer(ctk.CTkToplevel):

    def __init__(self, parent, imagePath):
        super().__init__(parent)
        self.geometry("700x700")
        self.attributes('-topmost', True)
        self.parent = parent
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, minsize=50)
        ctk.CTkLabel(self, text="", image=ctk.CTkImage(Image.open(imagePath), size=(600, 600))).grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ctk.CTkButton(self, text="OK", fg_color="green", width=75, command=self.quitter).grid(row=1, column=0, pady=5)
        self.wait_visibility()
        self.grab_set()

    def quitter(self):
        self.parent.deiconify()
        self.destroy()