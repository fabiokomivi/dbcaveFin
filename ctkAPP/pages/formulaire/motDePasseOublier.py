import copy
import customtkinter as ctk
from tkinter import filedialog
from .erreur.erreur import erreur
from PIL import Image
from controleur.employeControler import *
from controleur.chefControler import *
import re
import hashlib

import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

class motDePasseOublier(ctk.CTkToplevel):

    emailPattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("360x160")
        self.resizable(False, False)
        self.title("mot de passe oublier")
        self.centreFenetre()
        self.protocol("WM_DELETE_WINDOW", self.fermetureAnormale)
        self.attributes('-topmost', True)


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        topFrame = ctk.CTkFrame(self)
        
                
        topFrame.grid_columnconfigure(0, weight=0)
        topFrame.grid_columnconfigure(1, weight=1)
        topFrame.rowconfigure(0, weight=1)
        
        topFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(topFrame, text="recuperation de mot de passe").grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        ctk.CTkLabel(topFrame, text="email:").grid(row=1, column=0,padx=(25, 5), pady=10)
        self.entreeEmail = ctk.CTkEntry(topFrame, width=300, placeholder_text="email")
        
        self.entreeEmail.grid(row=1, column=1, padx=5, pady=10)
        
        confirmationFrame= ctk.CTkFrame(topFrame)
        confirmationFrame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        ctk.CTkButton(confirmationFrame, text="annuler", fg_color="red", command=self.fermetureAnormale).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(confirmationFrame, text="valider", fg_color="green", command=self.verification).pack(side="right", padx=10, pady=5)

        self.wait_visibility()
        self.grab_set()

    def verification(self):
        email = self.entreeEmail.get()
        email = email if re.match(self.emailPattern, email) else email+"@gmail.com"
        if not re.match(self.emailPattern, email):
            self.wait_window(erreur(self, "email invalide"))
        else:
            chef = obtenirChefPar(addresse=email)
            if chef:
                self.envoieEmail(chef.email, self.hasher(), True)
                self.destroy()
            else:
                employe = obtenirEmployePar(addresse=email)
                employe=employe[0]
                if employe:
                    self.envoieEmail(employe.addresse, self.hasher(), False)
                    self.destroy()
                else:
                    self.wait_window(erreur(self, "utilisateur inexistant"))
        
    def fermetureAnormale(self):
        self.destroy()

    def rougir(self, widget):
        widget.configure(fg_color = "red")
        self.after(1500, lambda:self.blanchir(widget))

    def blanchir(self, widget):
        widget.configure(fg_color="white")
   
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

    def aInternet(self):
        try:
            # Vérifier la connexion à un site public
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            return False
        

    def envoieEmail(self, email, password, user):
        if not self.aInternet():
            self.wait_window(erreur(self, "utilisateur inexistant"))
            return

        # Créer le message
        msg = MIMEMultipart()
        msg['From'] = "amouzoufabio@gmail.com"
        msg['To'] = email
        msg['Subject'] = "recuperation de mot de passe"

        # Ajouter le corps de l'e-mail
        msg.attach(MIMEText("votre nouveau mot de passe est: "+password[1], 'plain'))

        try:
            # Établir la connexion au serveur SMTP
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Activer la protection TLS
                server.login("amouzoufabio@gmail.com", "dxjc djdn pbhn anis ")  # Se connecter au compte
                server.send_message(msg)
                self.wait_window(erreur(self, "veuillez verifier\nvotre boite de reception"))
                if user:
                    modifierChef(email=email, password=password[0])
                else:
                    modifierEmploye(addresse=email, mdp=password[0])
        except Exception as e:
            print(e)
            self.wait_window(erreur(self, "une erreur s'est produite"))



    def hasher(self):
        length = random.randint(4, 8)  # Choisir une longueur entre 4 et 8
        characters = string.ascii_letters + string.digits  # Lettres majuscules, minuscules et chiffres
        password = ''.join(random.choice(characters) for i in range(length))  # Générer le mot de passe
        passwordNonHash = copy.copy(password)
        passwordBytes = password.encode('utf-8')
        passwordHash = hashlib.sha256(passwordBytes)
        return (passwordHash.hexdigest(), passwordNonHash)