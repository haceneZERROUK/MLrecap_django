from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, FormView, TemplateView
from .models import Movie
from dotenv import load_dotenv
import os
import json
import datetime


# Create your views here.


class DashboardView(View) : 
    
    template_name = "dashboard.html"
    context_object_name = "dashboard"
    
    def get(self, request):
        # D'abord récupérer tous les films programmés pour avoir les salles occupées
        all_movies = Movie.objects.all()
        programmed_movies = all_movies.filter(programmed=True)
        programmed_count = programmed_movies.count()
        occupied_rooms = [movie.programmed_room for movie in programmed_movies if movie.programmed_room is not None]

        # Ensuite récupérer les 10 derniers films
        movies_list = all_movies.order_by('-creation_date')[:10]

        context = {
            "movies_list": movies_list,
            "programmed_count": programmed_count,
            "occupied_rooms": occupied_rooms
        }
        return render(request, self.template_name, context)        
        
        
    def post(self, request):
        movie_id = request.POST.get("id")
        programmed_room = request.POST.get("programmed_room")

        movie = get_object_or_404(Movie, id=movie_id)

        if not movie.programmed:
            if programmed_room: 
                movie.programmed = True
                movie.programmed_room = programmed_room
                movie.programmation_start_date = datetime.date.today() + datetime.timedelta(days=(2 - datetime.date.today().weekday()) % 7)
                movie.programmation_end_date = movie.programmation_start_date + datetime.timedelta(days=7)
        else:
            # Si on déprogramme le film
            movie.programmed = False
            movie.programmed_room = None  # Réinitialiser la salle
            movie.programmation_start_date = None  # Optionnel : réinitialiser les dates
            movie.programmation_end_date = None

        movie.save()

        return redirect("dashboard")
    
    
class HomePageView(View):
    template_name = "homepage.html"

    def get(self, request):
        # Récupérer les films programmés et les trier par salle
        on_view_movies = Movie.objects.filter(programmed=True).order_by('programmed_room')

        context = {
            "on_view_movies": on_view_movies, 
        }
        
        return render(request, self.template_name, context)


