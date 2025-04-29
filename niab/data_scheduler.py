import os
import django
import time
import schedule
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import pytz


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

def job():
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Tentative {attempt} : Démarrage du chargement des données...")
            load_insert_data()
            print("Chargement initial terminé avec succès")
            break  # Succès, on sort de la boucle
        except Exception as e:
            print(f"Erreur lors du chargement initial (tentative {attempt}) : {e}")
            if attempt < max_attempts:
                print("Nouvelle tentative dans 30 secondes...")
                time.sleep(30)
            else:
                print("Échec après 5 tentatives. Passage à la suite.")


heure_lancement = "06:30"
jour_lancement = "tuesday"

print(f"Planification configurée: prochain chargement mardi à {heure_lancement} (heure de Paris)")

paris = pytz.timezone('Europe/Paris')
already_ran = False

while True:
    now_paris = datetime.now(paris)
    # Vérifie si c'est le bon jour et la bonne heure
    if (now_paris.strftime("%A").lower() == jour_lancement and
        now_paris.strftime("%H:%M") == heure_lancement and
        not already_ran):
        job()  # Appelle ta fonction de chargement
        already_ran = True  # Pour ne pas relancer plusieurs fois dans la même minute
    # Reset du flag une fois la minute passée
    if now_paris.strftime("%H:%M") != heure_lancement:
        already_ran = False
    # print(now_paris.strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(30)