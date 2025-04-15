# niab_app/load_fake_data.py
import os
import django
import random
from datetime import timedelta

# Configurez Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niab.settings')
django.setup()

from django.utils import timezone
from niab_app.models import Film, Projection, RapportHebdomadaire

def load_fake_data():
    # Supprimer les données existantes
    print("Suppression des données existantes...")
    Film.objects.all().delete()
    Projection.objects.all().delete()
    RapportHebdomadaire.objects.all().delete()

    # Liste de titres de films fictifs plus réalistes
    titres_films = [
        # Films d'action/aventure
        {"titre_fr": "Les Gardiens de l'Aube", "titre_original": "Guardians of Dawn", "categorie": "Action"},
        {"titre_fr": "Tempête de Feu", "titre_original": "Firestorm", "categorie": "Action"},
        {"titre_fr": "Le Dernier Rempart", "titre_original": "The Last Stand", "categorie": "Action"},
        {"titre_fr": "Chasseurs d'Ombres", "titre_original": "Shadow Hunters", "categorie": "Aventure"},

        # Drames
        {"titre_fr": "Les Murmures du Passé", "titre_original": "Whispers of the Past", "categorie": "Drame"},
        {"titre_fr": "Souvenirs d'Automne", "titre_original": "Autumn Memories", "categorie": "Drame"},
        {"titre_fr": "Le Temps d'un Regard", "titre_original": "A Moment's Glance", "categorie": "Drame"},

        # Comédies
        {"titre_fr": "Vacances Catastrophe", "titre_original": "Vacation Disaster", "categorie": "Comédie"},
        {"titre_fr": "Le Mariage de Trop", "titre_original": "One Wedding Too Many", "categorie": "Comédie"},
        {"titre_fr": "Mes Voisins les Extraterrestres", "titre_original": "My Alien Neighbors", "categorie": "Comédie"},

        # Science-fiction
        {"titre_fr": "Chroniques Martiennes", "titre_original": "Martian Chronicles", "categorie": "Science-fiction"},
        {"titre_fr": "Nexus 2099", "titre_original": "Nexus 2099", "categorie": "Science-fiction"},
        {"titre_fr": "L'Éveil des Machines", "titre_original": "Rise of the Machines", "categorie": "Science-fiction"},

        # Horreur
        {"titre_fr": "La Maison des Ombres", "titre_original": "House of Shadows", "categorie": "Horreur"},
        {"titre_fr": "Murmures Nocturnes", "titre_original": "Night Whispers", "categorie": "Horreur"},
        {"titre_fr": "Le 13ème Étage", "titre_original": "The 13th Floor", "categorie": "Horreur"},

        # Animation
        {"titre_fr": "Les Aventures de Milo", "titre_original": "Milo's Adventures", "categorie": "Animation"},
        {"titre_fr": "Le Royaume des Dragons", "titre_original": "Dragon Kingdom", "categorie": "Animation"},
        {"titre_fr": "Étoiles Filantes", "titre_original": "Shooting Stars", "categorie": "Animation"},

        # Thriller
        {"titre_fr": "Derrière les Apparences", "titre_original": "Behind the Appearances", "categorie": "Thriller"},
        {"titre_fr": "Code Silence", "titre_original": "Code Silence", "categorie": "Thriller"},
        {"titre_fr": "L'Énigme du Lac", "titre_original": "The Lake Mystery", "categorie": "Thriller"},
    ]

    # Classifications d'âge
    classifications = ["Tous publics", "10+", "12+", "16+", "18+"]

    # Pays
    pays = ["France", "États-Unis", "Royaume-Uni", "Japon", "Corée du Sud",
           "Allemagne", "Espagne", "Italie", "Canada", "Australie"]

    # Mélanger la liste des titres
    random.shuffle(titres_films)

    # Limiter à 10 films
    titres_films = titres_films[:10]

    # Créer les films
    films = []
    for i, film_info in enumerate(titres_films):
        # Déterminer si c'est un film passé ou futur
        is_future = random.choice([True, False])

        if is_future:
            # Film à venir (date dans le futur)
            date = timezone.now() + timedelta(days=random.randint(7, 90))
            entrees_totales = None
            entrees_hebdomadaires = None
            recettes_box_office = None
            benefice = None
        else:
            # Film déjà sorti
            date = timezone.now() - timedelta(days=random.randint(1, 60))
            entrees_totales = random.randint(10000, 500000)
            entrees_hebdomadaires = random.randint(5000, 100000)
            recettes_box_office = random.randint(1000000, 500000000)
            benefice = random.randint(-50000000, 300000000)

        # Durée aléatoire entre 80 et 180 minutes
        duree_minutes = random.randint(80, 180)
        duree = timedelta(minutes=duree_minutes)

        # Budget entre 5 et 250 millions
        budget = random.randint(5000000, 250000000)

        # Année de sortie
        annee_sortie = str(date.year)

        # Créer le film
        film = Film.objects.create(
            titre_fr=film_info["titre_fr"],
            titre_original=film_info["titre_original"],
            pays=random.choice(pays),
            categorie=film_info["categorie"],
            annee_sortie=annee_sortie,
            date=date,
            PEGI=random.choice(classifications),
            duree=duree,
            duree_minutes=duree_minutes,
            entrees_totales=entrees_totales,
            entrees_hebdomadaires=entrees_hebdomadaires,
            nom=film_info["titre_fr"].split()[0],  # Premier mot du titre
            budget=budget,
            recettes_box_office=recettes_box_office,
            benefice=benefice,
            rentabilite="Rentable" if benefice and benefice > 0 else "Non rentable",
            entrees_prevues=random.randint(50000, 300000),
            url_miniature=""
        )

        films.append(film)
        print(f"Film créé: {film.titre_fr}")

    # Créer des projections pour les films déjà sortis
    # Utiliser une combinaison unique de salle et semaine pour chaque projection
    past_films = [film for film in films if film.date <= timezone.now()]

    # Limiter le nombre de projections à créer
    num_projections = min(len(past_films), 5)  # Maximum 5 projections

    for i in range(num_projections):
        if i < len(past_films):
            film = past_films[i]
            # Utiliser une semaine différente pour chaque projection
            semaine = timezone.now() - timedelta(days=7 * (i + 1))

            # Créer une projection
            Projection.objects.create(
                film=film,
                numero_salle=i + 1,  # Salle différente pour chaque projection
                semaine_debutant=semaine,
                audience_quotidienne_estimee=random.randint(100, 500),
                audience_quotidienne_reelle=random.randint(100, 500),
                prix_par_billet=random.choice([8.50, 9.00, 10.00, 12.50])
            )
            print(f"Projection créée pour: {film.titre_fr} (Salle {i+1}, Semaine du {semaine.strftime('%d/%m/%Y')})")

    # Créer un rapport hebdomadaire
    # Notez que nous ne définissons pas le champ 'benefice' car c'est une propriété calculée
    revenus = random.randint(8000, 20000)
    couts = random.randint(3000, 8000)

    RapportHebdomadaire.objects.create(
        semaine_debutant=timezone.now() - timedelta(days=7),
        revenus_totaux=revenus,
        couts_totaux=couts,
        taux_occupation=random.uniform(50.0, 95.0),
        precision_prediction=random.uniform(70.0, 99.0)
    )
    print("Rapport hebdomadaire créé")

    print("Données fictives chargées avec succès!")

if __name__ == "__main__":
    load_fake_data()