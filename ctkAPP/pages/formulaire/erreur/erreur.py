import customtkinter as ctk

class erreur(ctk.CTkToplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title("")
        self.attributes('-topmost', True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=50)
        frame = ctk.CTkFrame(self, fg_color="#E6E6E6")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(0, minsize=50)
        frame.grid(row=0, column=0,padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(frame, text=message).grid(column=0, row=0, padx=3, pady=0)
        ctk.CTkButton(self, text="ok", command=self.destroy).grid(column=0, row=1, padx=3, pady=5)

        self.centreFenetre()
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()
        self.after(3000, self.destroy)

    def centreFenetre(self):

        pere_x = self.master.winfo_x()
        pere_y = self.master.winfo_y()
        pere_largeur = self.master.winfo_width()
        pere_hauter = self.master.winfo_height()

        enfant_largeur = self.winfo_reqwidth()
        enfant_hauteur = self.winfo_reqheight()

        position_x = pere_x + (pere_largeur // 2) - (enfant_largeur // 2)
        position_y = pere_y + (pere_hauter // 2) - (enfant_hauteur // 2)

        self.geometry(f"+{position_x}+{position_y}")