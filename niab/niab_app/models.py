from django.db import models

# Create your models here.


class Movie(models.model) : 
    
    fr_title = models.TextField()
    original_title = models.CharField()
    released_date = models.DateField()
    casting = models.TextField()
    director = models.CharField()
    writer = models.CharField()
    distribution = models.CharField()
    country = models.CharField()
    classification = models.CharField()
    duration = models.CharField()
    categories = models.TextField()                     # scraping récupérer toutes les catégories
    weekly_entrances_pred = models.IntegerChoices()
    synopsis = models.TextField()
    programmed = models.BooleanField()
    programmation_start_date = models.DateField()
    programmation_end_date = models.DateField()
    image_url = models.CharField()
    










