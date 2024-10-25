from setuptools import setup, find_packages

setup(
    name='GestionCave',  # Nom de ton application
    version='0.1',  # Version de ton application
    description='Application de gestion de cave avec Tkinter',  # Description
    author='Ton Nom',  # Remplace par ton nom
    author_email='tonemail@example.com',  # Remplace par ton email
    packages=find_packages(),  # Trouve tous les packages automatiquement
    entry_points={
        'gui_scripts': [
            'gestioncave=app:main',  # Assure-toi que 'main' est le nom de ton fichier et 'main' est la fonction principale
        ],
    },
    install_requires=[
        # Liste des dépendances requises par ton application
        # par exemple, 'sqlalchemy', 'psycopg2', si tu utilises des bases de données
        'sqlalchemy', 'psycopg2', 'weasyprint', 'tkcalendar', 'tkinter', 'customtkinter'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Version minimum de Python requise
)

python setup.py sdist
pip install ./dist/GestionCave-0.1.tar.gz
gestioncave
