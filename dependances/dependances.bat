@echo off

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé. Veuillez installer Python avant de continuer.
    pause
    exit /b
)

:: Installer les bibliothèques Python avec pip
pip install customtkinter sqlalchemy psycopg2 weasyprint matplotlib tkcalendar
