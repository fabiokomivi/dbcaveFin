#!/bin/bash

# Mettre à jour les paquets
sudo apt update

# Installer les dépendances système pour certaines bibliothèques
sudo apt install -y python3-pip python3-tk libpq-dev libffi-dev libgtk-3-dev libcairo2

# Installer les bibliothèques Python
pip3 install customtkinter sqlalchemy psycopg2 weasyprint matplotlib tkcalendar
