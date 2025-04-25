import json
from datetime import datetime
from dotenv import load_dotenv
import os
import time
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from niab.niab_app.models import Movie
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niab.settings')
django.setup()

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")

account_name = os.getenv("ACCOUNT_NAME")
account_key = os.getenv("ACCOUNT_KEY")
container_name = os.getenv("CONTAINER_NAME")
blob_name = os.getenv("saving_file")

# Création du service d'accès aux blobs
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# blob de destination
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name+".json")

# téléchargement du fichier
with open(blob_name+".json", "wb") as download_file:
    download_data = blob_client.download_blob()
    download_file.write(download_data.readall())

####################################################################################    
####################################################################################    



time.sleep(5)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

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




    
    
####################################################################################    
####################################################################################    

# # Connexion à la base de données MySQL (avec retry)
# for i in range(10):
#     try:
#         conn = mysql.connector.connect(
#             host=DATABASE_HOST,
#             port=DATABASE_PORT,
#             user=DATABASE_USERNAME,
#             password=DATABASE_PASSWORD,
#             database=DATABASE_NAME
#         )
#         break
#     except mysql.connector.Error as err:
#         print(f"Tentative {i+1}/10 : MySQL pas prêt ({err}), attente 3s...")
#         time.sleep(3)
# else:
#     print("Impossible de se connecter à MySQL après plusieurs tentatives.")
#     exit(1)

# cursor = conn.cursor()

# # Charger les données du fichier JSON
# with open('/django_app/upcomes.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Préparer la requête d'insertion
# sql = """
# INSERT INTO niab_app_movie (
#     fr_title, original_title, released_date, casting, director, writer, distribution, country,
#     classification, duration, categories, weekly_entrances_pred, synopsis, programmed,
#     programmed_room, programmation_start_date, programmation_end_date, allocine_url,
#     image_url, trailer_url, creation_date
# ) VALUES (
#     %s, %s, %s, %s, %s, %s, %s, %s,
#     %s, %s, %s, %s, %s, %s,
#     %s, %s, %s, %s,
#     %s, %s, %s
# )
# """

# for movie in data:
#     # Conversion de la date au format YYYY-MM-DD
#     try:
#         released_date = datetime.strptime(movie.get('released_date', ''), '%d/%m/%Y').date()
#     except Exception:
#         released_date = None

#     # Champs à remplir ou à générer
#     casting = ', '.join([a for a in [movie.get('actor_1'), movie.get('actor_2'), movie.get('actor_3')] if a and a != "no_actor"])
#     director = movie.get('director') or movie.get('directors') or ''
#     categories = ', '.join(movie.get('list_categories', [])) if 'list_categories' in movie else movie.get('category', '')
#     synopsis = movie.get('synopsis', None).strip()
#     weekly_entrances_pred = 1000  # Valeur arbitraire, à modifier selon besoin

#     # Préparer les valeurs dans le même ordre que la requête
#     values = (
#         movie.get('fr_title', ''),
#         movie.get('original_title', ''),
#         released_date,
#         casting,
#         director,
#         movie.get('writer', ''),
#         movie.get('distribution', ''),
#         movie.get('country', ''),
#         movie.get('classification', ''),
#         movie.get('duration', ''),
#         categories,
#         weekly_entrances_pred,
#         synopsis,
#         False,         
#         None,          
#         None,          
#         None,          
#         movie.get('allocine_url', ''),
#         movie.get('image_url', ''),
#         None,          
#         datetime.now().date()
#     )
#     cursor.execute(sql, values)

# conn.commit()
# cursor.close()
# conn.close()

