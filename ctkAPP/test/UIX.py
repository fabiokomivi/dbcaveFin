import customtkinter as ctk
from PIL import Image

# Initialiser CustomTkinter
ctk.set_appearance_mode("dark")  # Mode sombre
ctk.set_default_color_theme("/home/fabio/Bureau/python/appCTKenv/ctkAPP/themes/green.json")  # Thème bleu

class Record(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Créer un label centré
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.grid(row=0, column=0, padx=100, pady=50, sticky="nsew")

        #label = ctk.CTkLabel(self, text="enregistrement", font=("Arial", 36), bg_color="pink")
        #label.grid(row=0, column=0, padx=20, pady=50, sticky="ew")

        self.entryIne = ctk.CTkEntry(self.container, placeholder_text="entrer votre ine", fg_color="red")
        self.entryIne.grid(row=1, column=0, padx=10, pady=10)

        self.entryNom = ctk.CTkEntry(self.container, placeholder_text="entrer votre nom", fg_color="white")
        self.entryNom.grid(row=2, column=0, padx=10, pady=10)

        self.entryPrenom= ctk.CTkEntry(self.container, placeholder_text="entrer votre prenom", fg_color="green")
        self.entryPrenom.grid(row=3, column=0, padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Configurer la grille pour que le label soit centré


class DashBoard(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Créer un label centré
        label = ctk.CTkLabel(self, text="enregistrement", font=("Arial", 36), bg_color="pink")
        label.grid(row=0, column=0, padx=100, pady=100, sticky="ew")

        self.entryIne = ctk.CTkEntry(self, placeholder_text="entrer votre ine", fg_color="red")
        self.entryIne.grid(row=1, column=0, padx=10, pady=10)

        self.entryNom = ctk.CTkEntry(self, placeholder_text="entrer votre nom", fg_color="white")
        self.entryNom.grid(row=2, column=0, padx=10, pady=10)

        self.entryPrenom= ctk.CTkEntry(self, placeholder_text="entrer votre prenom", fg_color="green")
        self.entryPrenom.grid(row=3, column=0, padx=10, pady=10)

        # Configurer la grille pour que le label soit centré
      


class APP(ctk.CTk):

    listdImage = ctk.CTkImage(Image.open("/home/fabio/Bureau/python/appCTKenv/ctkAPP/images/list.png"), size=(30, 30))
    dashboardImage = ctk.CTkImage(Image.open("/home/fabio/Bureau/python/appCTKenv/ctkAPP/images/dashboard.png"), size=(30, 30))
    userImage = ctk.CTkImage(Image.open("/home/fabio/Bureau/python/appCTKenv/ctkAPP/images/user.png"), size=(30, 30))
    updateImage = ctk.CTkImage(Image.open("/home/fabio/Bureau/python/appCTKenv/ctkAPP/images/update.png"), size=(30, 30))
    deleteImage = ctk.CTkImage(Image.open("/home/fabio/Bureau/python/appCTKenv/ctkAPP/images/delete.png"), size=(30, 30))
    exitImage = ctk.CTkImage(Image.open("/home/fabio/Bureau/python/appCTKenv/ctkAPP/images/exit.png"), size=(30, 30))
    settingImage = ctk.CTkImage(Image.open("/home/fabio/Bureau/python/appCTKenv/ctkAPP/images/settings.png"), size=(30, 30))

    def __init__(self):
        super().__init__()

        self.geometry("1200x650")
        self.title("cellar manager")

        # Menu sur le côté gauche
        self.initMenu()
        # Zone de contenu à droite
        self.initContent()
        self.switch = ctk.CTkSwitch(self, text="dark", command=self.setTheme)
        self.switch.grid(row=1, column=0)

        # Configurer la grille du cadre de contenu
        

        # Page de bienvenue
        
        self.pages = {}

        self.mainloop()

    def initMenu(self):
        self.menu = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#2A2A2A")
        self.menu.grid_columnconfigure(0, weight=1)
        self.menu.grid_propagate(False)
        self.menu.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(self.menu ,text="menu", text_color="white", font=("Arial", 40)).grid(row=0, column=0, padx=5, sticky=("ew"), pady=(10, 15))

        self.goDashboad = ctk.CTkButton(self.menu, text="dashboard", font=("Arial", 20), border_color="white", text_color="#473ec8", fg_color="#AECEE4", border_width=2, corner_radius=10, image=self.dashboardImage)
        self.goDashboad.grid(row=1, column=0, pady=(10, 10), padx=10, sticky="ew")

        self.goRecord = ctk.CTkButton(self.menu, text="recording", font=("Arial", 20), border_color="white", text_color="#473ec8", fg_color="#AECEE4", border_width=2, corner_radius=10, image=self.userImage)
        self.goRecord.grid(row=2, column=0, pady=(10, 10), padx=10, sticky="ew")

        self.goUpdate = ctk.CTkButton(self.menu, text="  updating", font=("Arial", 20), border_color="white", text_color="#473ec8", fg_color="#AECEE4", border_width=2, corner_radius=10, image=self.updateImage)
        self.goUpdate.grid(row=3, column=0, pady=(10, 10), padx=10, sticky="ew")

        self.goDelete = ctk.CTkButton(self.menu, text=" deleting   ", font=("Arial", 20), border_color="white", text_color="#473ec8", fg_color="#AECEE4", border_width=2, corner_radius=10, image=self.deleteImage)
        self.goDelete.grid(row=4, column=0, pady=(10, 10), padx=10, sticky="ew")

        self.goView = ctk.CTkButton(self.menu, text=" viewing   ", image=self.listdImage)
        self.goView.grid(row=5, column=0, pady=(10, 10), padx=10, sticky="ew")

        self.settings = ctk.CTkButton(self.menu, text=" settings   ", border_width=2, corner_radius=10, image=self.settingImage)
        self.settings.grid(row=6, column=0, pady=(150, 10), padx=10, sticky="ew")

        ctk.CTkButton(self.menu, text="  quit   ", font=("Arial", 20), border_color="white", fg_color="red", border_width=2, corner_radius=10, command=self.quit, image=self.exitImage).grid(row=7, column=0, pady=(10, 10), padx=10, sticky="ew")

        

    def initContent(self):
        self.content = ctk.CTkFrame(self, corner_radius=10, fg_color="#333333")
        self.content.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)#

        # Configurer la grille pour que le contenu prenne tout l'espace disponible
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.welcome_page = Record(parent=self.content, controller=self)
        self.welcome_page.grid(row=0, column=0, rowspan=2, sticky="nsew", pady=15, padx=15)
        self.welcome_page.tkraise()  # Mettre la frame au premier plan
    
    def setTheme(self):
        if self.switch.get():
            self.switch.configure(text="light")
            ctk.set_appearance_mode("light")
            #ctk.set_default_color_theme("blue")

        else:
            self.switch.configure(text="dark")
            ctk.set_appearance_mode("dark")
            #ctk.set_default_color_theme("green")

    def initPages(self):
        pass




# Lancer l'application
APP()
