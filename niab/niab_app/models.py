from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

class User(AbstractUser):
    """
    Modèle représentant un utilisateur de l'application cinéma.
    """
    prenom = models.CharField("Prénom", max_length=150, blank=True)
    nom = models.CharField("Nom", max_length=150, blank=True)
    telephone = models.CharField(max_length=10, null=True, default='0000000000')
    poste = models.CharField(max_length=100, null=True, default="Staff")
    est_manager = models.BooleanField(default=False)
    est_membre_personnel = models.BooleanField(default=False)

class Film(models.Model):
    """
    Modèle représentant un film dans le système.
    """
    titre_fr = models.CharField(max_length=255)
    titre_original = models.CharField(max_length=255)
    pays = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    annee_sortie = models.CharField(max_length=4)
    date = models.DateField()
    PEGI = models.CharField(max_length=50)
    duree = models.DurationField()
    duree_minutes = models.FloatField()
    entrees_totales = models.IntegerField(null=True, blank=True)
    entrees_hebdomadaires = models.IntegerField(null=True, blank=True)
    nom = models.CharField(max_length=255)
    budget = models.BigIntegerField(null=True, blank=True)
    recettes_box_office = models.BigIntegerField(null=True, blank=True)
    benefice = models.BigIntegerField(null=True, blank=True)
    rentabilite = models.CharField(max_length=50, null=True, blank=True)
    entrees_prevues = models.IntegerField(null=True, blank=True)
    date_prediction = models.DateTimeField(auto_now_add=True)
    url_miniature = models.URLField(blank=True)

    def __str__(self):
        return f"{self.titre_fr} ({self.annee_sortie})"

    def save(self, *args, **kwargs):
        if self.duree and not self.duree_minutes:
            self.duree_minutes = self.duree.total_seconds() / 60
        super().save(*args, **kwargs)

class Projection(models.Model):
    """
    Modèle représentant une projection de film.
    """
    CHOIX_SALLES = [
        (1, 'Salle 1 (120 places)'),
        (2, 'Salle 2 (80 places)'),
    ]

    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    numero_salle = models.IntegerField(choices=CHOIX_SALLES)
    semaine_debutant = models.DateField()
    audience_quotidienne_estimee = models.IntegerField()
    audience_quotidienne_reelle = models.IntegerField(null=True, blank=True)
    prix_par_billet = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=10.00
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['numero_salle', 'semaine_debutant'],
                name='unique_screening_room_week'
            )
        ]

    def __str__(self):
        return f"{self.film.titre_fr} - Salle {self.numero_salle} - Semaine du {self.semaine_debutant}"

class RapportHebdomadaire(models.Model):
    """
    Modèle représentant un rapport hebdomadaire.
    """
    semaine_debutant = models.DateField(unique=True)
    revenus_totaux = models.DecimalField(max_digits=10, decimal_places=2)
    couts_totaux = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=4900.00
    )
    taux_occupation = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    precision_prediction = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )

    @property
    def benefice(self):
        return self.revenus_totaux - self.couts_totaux

    def __str__(self):
        return f"Rapport semaine du {self.semaine_debutant}"