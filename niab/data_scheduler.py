import os
import django
import time
import schedule
from dotenv import load_dotenv, find_dotenv

# Importer la fonction du premier script
from data_load_once import load_insert_data

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niab.settings')
django.setup()

# Chargement des variables d'environnement
dot_env_path = find_dotenv()
load_dotenv(dotenv_path=dot_env_path, override=True)

# Configuration du planificateur
print("Démarrage du planificateur de chargement des données...")
schedule.every().thursday.at("06:30").do(load_insert_data)
print(f"Planification configurée: prochain chargement jeudi à 06:30")

# Boucle infinie (dans un processus détaché)
while True:
    schedule.run_pending()
    time.sleep(60)
