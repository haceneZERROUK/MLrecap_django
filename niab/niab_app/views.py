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
from .forms import ContactForm, GuestUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.


class DashboardView(View) : 
    
    template_name = "dashboard.html"
    context_object_name = "dashboard"
    
    def get(self, request):
        if not request.user.is_authenticated:
            response = render(request, "401.html", status=401)
            response['WWW-Authenticate'] = 'Form'
            return response

        all_movies = Movie.objects.all()
        programmed_movies = all_movies.filter(programmed=True)

        # Récupérer les 10 derniers films
        movies_list = all_movies.order_by('-creation_date')[:10]

        # Trouver la date de création la plus récente parmi les films programmés
        if programmed_movies.exists():
            max_programmed_creation_date = programmed_movies.order_by('-creation_date').first().creation_date
            # Si un des 10 derniers films est plus récent que les films programmés, on déprogramme tout
            if any(movie.creation_date > max_programmed_creation_date for movie in movies_list):
                for movie in programmed_movies:
                    movie.programmed = False
                    movie.programmed_room = None
                    movie.programmation_start_date = None
                    movie.programmation_end_date = None
                    movie.save()
                # Recharger la liste après déprogrammation
                programmed_movies = all_movies.filter(programmed=True)

        programmed_count = programmed_movies.count()
        occupied_rooms = [movie.programmed_room for movie in programmed_movies if movie.programmed_room is not None]

        # Ajout de la variable calculée à chaque film
        for movie in movies_list:
            if movie.weekly_entrances_pred:
                movie.predicted_revenue = movie.weekly_entrances_pred * 0.005  # équivalent à (1/2000)*10
            else:
                movie.predicted_revenue = None

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



class ContactView(View):
    template_name = "contact.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = f"Nouveau message de contact de {nom}"
        message_body = f"Nom: {nom}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject,
            message_body,
            settings.EMAIL_HOST_USER,  # expéditeur (défini dans settings.py)
            [settings.DEFAULT_TO_EMAIL],
            # ['malek.boumedine@gmail.com'],  # destinataire
            fail_silently=False,
        )

        # On peut afficher un message de succès ou rediriger
        context = {"success": True}
        return render(request, self.template_name, context)
        
    
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



class MoviesHistoryView(View):
    template_name = "predictions_history.html"
    context_object_name = "predictions_history"

    def get(self, request):
        # Récupérer toutes les dates de création distinctes, groupées par semaine ISO
        movies = Movie.objects.all().order_by('-creation_date')
        weeks = movies.values_list('creation_date', flat=True).distinct()

        # Construire une liste de tuples (année, semaine, date_debut_semaine_mardi)
        week_choices = set()
        for d in weeks:
            iso = d.isocalendar()
            week_choices.add((iso[0], iso[1]))
        week_choices_with_dates = []
        for year, week in week_choices:
            # Calcule le lundi de la semaine
            monday = datetime.datetime.strptime(f'{year}-W{week}-1', "%G-W%V-%u").date()
            # Décale d'un jour pour avoir mardi
            tuesday = monday + timedelta(days=1)
            week_choices_with_dates.append((year, week, tuesday))
        week_choices_with_dates = sorted(week_choices_with_dates, reverse=True)

        # Par défaut, afficher la semaine la plus récente
        selected_year, selected_week = (week_choices_with_dates[0][0], week_choices_with_dates[0][1]) if week_choices_with_dates else (None, None)
        if 'week' in request.GET:
            selected = request.GET['week']
            try:
                selected_year, selected_week = map(int, selected.split('-W'))
            except Exception:
                pass

        # Calculer le début (mardi) et la fin (lundi suivant) de la semaine sélectionnée
        if selected_year and selected_week:
            monday = datetime.datetime.strptime(f'{selected_year}-W{selected_week}-1', "%G-W%V-%u").date()
            tuesday = monday + timedelta(days=1)
            next_monday = monday + timedelta(days=7)
            movies_list = movies.filter(creation_date__gte=tuesday, creation_date__lt=next_monday)
        else:
            movies_list = Movie.objects.none()

        # Compter les films programmés et les salles occupées (si besoin pour le template)
        programmed_movies = Movie.objects.filter(programmed=True)
        programmed_count = programmed_movies.count()
        occupied_rooms = [movie.programmed_room for movie in programmed_movies if movie.programmed_room is not None]

        context = {
            "week_choices": week_choices_with_dates,
            "selected_year": selected_year,
            "selected_week": selected_week,
            "movies_list": movies_list,
            "programmed_count": programmed_count,
            "occupied_rooms": occupied_rooms,
        }
        return render(request, self.template_name, context)
    

def admin_required(user):
    return user.is_superuser

@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class CreateGuestUserView(View):
    template_name = "create_guest_user.html"
    context_object_name = "create_guest_user"

    def get(self, request):
        form = GuestUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = GuestUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {"form": GuestUserCreationForm(), "success": True})
        return render(request, self.template_name, {"form": form})
    
    
class AboutUsView(TemplateView):
    template_name = "about_us.html"
    context_object_name = "about_us"
    
    