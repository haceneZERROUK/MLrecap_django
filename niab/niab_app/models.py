from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
import django


# Create your models here.


class Movie(models.Model) : 
    
    fr_title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    released_date = models.DateField(null=False)
    casting = models.TextField()
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    distribution = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    classification = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    categories = models.TextField()                     # scraping récupérer toutes les catégories
    weekly_entrances_pred = models.IntegerField(null=True)
    synopsis = models.TextField(null=True)
    programmed = models.BooleanField(default=False)
    programmed_room = models.IntegerField(choices=[(1, "Salle 1"), (2, "Salle 2")], null=True)
    programmation_start_date = models.DateField(null=True)
    programmation_end_date = models.DateField(null=True)
    allocine_url =  models.URLField(max_length=500, null=True, blank=True, verbose_name="URL allocine")
    image_url = models.URLField(max_length=500, null=True, blank=True, verbose_name="URL de l'image")
    trailer_url = models.URLField(max_length=500, null=True, blank=True, verbose_name="URL de la bande-annonce")
    creation_date = models.DateField(auto_now_add=True)
    

class User(AbstractUser) : 
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)








