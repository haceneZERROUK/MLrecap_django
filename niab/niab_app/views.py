from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, FormView, TemplateView
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import models
from django.urls import reverse_lazy
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
        # récupérer tous les films programmés pour avoir les salles occupées
        all_movies = Movie.objects.all()
        programmed_movies = all_movies.filter(programmed=True)
        programmed_count = programmed_movies.count()
        occupied_rooms = [movie.programmed_room for movie in programmed_movies if movie.programmed_room is not None]

        # récupérer les 10 derniers films
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
    context_object_name = "homepage"
    
    def get(self, request):
        on_view_movies = Movie.objects.filter(programmed=True).order_by('-creation_date')[:2]

        context = {
            "on_view_movies": on_view_movies,
        }
        return render(request, self.template_name, context)



class MyLoginView(LoginView) : 
    
    template_name = "registration/login.html"
    context_object_name = "login"
    
    redirect_authenticated_user = True
    success_url = reverse_lazy("dashboard")

    def get_success_url(self) : 
        return self.success_url


def logout_view(request):
    logout(request)
    return redirect('homepage')



class ContactView(View) : 
    
    template_name = "contact.html"
    context_object_name = "contact"

    def get(self, request) : 
        
        return render(request, self.template_name)
        pass
    
    def post(self, request) : 
        
        pass



UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentifie avec le username OU l'email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            # Cherche un utilisateur avec username OU email
            user = UserModel.objects.get(
                models.Q(username__iexact=username) | models.Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            # Pas d'utilisateur trouvé
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None







