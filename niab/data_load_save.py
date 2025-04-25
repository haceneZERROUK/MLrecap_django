import json
from datetime import datetime
from dotenv import load_dotenv
import time
from azure.storage.blob import BlobServiceClient
from niab_app.models import Movie
from django.db import transaction
import os
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niab.settings')
django.setup()

dotenv_path = "../.env"
load_dotenv(dotenv_path=dotenv_path)

account_name = os.getenv("ACCOUNT_NAME")
account_key = os.getenv("ACCOUNT_KEY")
container_name = os.getenv("CONTAINER_NAME")
blob_name = os.getenv("saving_file")

blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net",credential=account_key)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name + ".json")

json_path = blob_name + ".json"

try:
    with open(json_path, "wb") as download_file:
        download_data = blob_client.download_blob()
        download_file.write(download_data.readall())
    print("Fichier téléchargé, début import...")
except ModuleNotFoundError:
    print(f"ERREUR : Le fichier {blob_name}.json n'existe pas dans le conteneur {container_name}.")
    exit(1)
except Exception as e:
    print(f"ERREUR inattendue lors du téléchargement du blob : {e}")
    exit(1)

########################################################################

# insertion des données dans la BDD
time.sleep(2)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)


with transaction.atomic():
    for movie in data:
        try:
            released_date = datetime.strptime(movie.get('released_date', ''), '%d/%m/%Y').date()
        except Exception:
            released_date = None

        casting = ', '.join(
            [a for a in [movie.get('actor_1'), movie.get('actor_2'), movie.get('actor_3')] if a and a != "no_actor"]
        )
        director = movie.get('director') or movie.get('directors') or ''
        categories = ', '.join(movie.get('list_categories', [])) if 'list_categories' in movie else movie.get('category', '')
        synopsis = movie.get('synopsis', None)
        if synopsis:
            synopsis = synopsis.strip()

        weekly_entrances_pred = 10000

        Movie.objects.create(
            fr_title=movie.get('fr_title', ''),
            original_title=movie.get('original_title', ''),
            released_date=released_date,
            casting=casting,
            director=director,
            writer=movie.get('writer', ''),
            distribution=movie.get('distribution', ''),
            country=movie.get('country', ''),
            classification=movie.get('classification', ''),
            duration=movie.get('duration', ''),
            categories=categories,
            weekly_entrances_pred=weekly_entrances_pred,
            synopsis=synopsis,
            programmed=False,
            programmed_room=None,
            programmation_start_date=None,
            programmation_end_date=None,
            allocine_url=movie.get('allocine_url', ''),
            image_url=movie.get('image_url', ''),
            trailer_url=None
        )
        print(f"Film importé : {movie.get('fr_title', '')}")

print("Import terminé !")

