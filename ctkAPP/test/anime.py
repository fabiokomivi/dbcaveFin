import tkinter as tk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Exemple avec place et étendre en Tkinter")

        # Créer un frame qui va s'étendre
        self.frame = tk.Frame(self, bg="lightblue")
        
        # Utiliser place avec relwidth et relheight pour étendre le frame
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # relwidth=1 et relheight=1 signifie qu'il prend tout l'espace

        # Ajouter un bouton pour vérifier que le frame fonctionne
        self.bouton = tk.Button(self.frame, text="Ceci est un bouton")
        self.bouton.place(relx=0.5, rely=0.5, anchor="center")  # Positionner le bouton au centre

# Lancer l'application
if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
