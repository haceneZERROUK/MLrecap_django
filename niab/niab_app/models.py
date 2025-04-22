from django.db import models

# Create your models here.


class Movie(models.Model) : 
    
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
    weekly_entrances_pred = models.IntegerField(null=True)
    synopsis = models.TextField(null=True)
    programmed = models.BooleanField(default=False)
    programmed_room = models.IntegerField(choices=[(1, "Room 1"), (2, "Room 2")], null=True)
    programmation_start_date = models.DateField(null=True)
    programmation_end_date = models.DateField(null=True)
    allocine_url = models.CharField(null=True)
    image_url = models.CharField(null=True)
    










