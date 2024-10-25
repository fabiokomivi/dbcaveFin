import customtkinter as ctk

class Confirmation(ctk.CTkToplevel):
    def __init__(self, parent, message, callback):
        super().__init__(parent)
        self.title("")
        self.protocol("WM_DELETE_WINDOW", self.fermetureAnormale)
        self.attributes('-topmost', True)
        self.callback = callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=50)

        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, columnspan=2,padx=5, pady=5, sticky="nsew")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)


        ctk.CTkLabel(frame, text=message, corner_radius=10, fg_color="#E6E6E6").grid(column=0, row=0, columnspan=2, padx=3, pady=10)
        ctk.CTkButton(self, text="continuer", fg_color="red", command=self.accepter).grid(column=1, row=1, padx=3, pady=5, sticky="nsew")
        ctk.CTkButton(self, text="arreter", fg_color="green", command=self.decliner).grid(column=0, row=1, padx=3, pady=5, sticky="nsew")

        self.centreFenetre()
        self.resizable(False, False)

        self.wait_visibility()

        self.grab_set()

    def accepter(self):
        self.callback(True)
        self.destroy()

    def decliner(self):
        self.callback(False)
        self.destroy()


    def fermetureAnormale(self):
        self.callback(False)
        self.destroy()

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
