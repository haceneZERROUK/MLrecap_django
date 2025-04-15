from django.shortcuts import render

# niab_app/views.py

from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Film, Projection, RapportHebdomadaire
from django.utils import timezone
from datetime import timedelta

class HomePageView(TemplateView):
    template_name = 'niab_app/home.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'niab_app/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer les 10 prochains films
        next_wednesday = timezone.now() + timedelta(days=(2 - timezone.now().weekday() + 7) % 7)
        context['upcoming_movies'] = Film.objects.filter(
            date__gte=next_wednesday
        ).order_by('date')[:10]

        # Films actuellement projetés
        context['current_screenings'] = Projection.objects.filter(
            semaine_debutant__lte=timezone.now(),
            semaine_debutant__gte=timezone.now() - timedelta(days=7)
        ).select_related('film')

        # Statistiques hebdomadaires
        current_week = RapportHebdomadaire.objects.filter(
            semaine_debutant__lte=timezone.now()
        ).order_by('-semaine_debutant').first()

        if current_week:
            context['weekly_stats'] = {
                'revenue': current_week.revenus_totaux,
                'costs': current_week.couts_totaux,
                'profit': current_week.benefice,
                'occupancy_rate': current_week.taux_occupation,
            }

        return context

class FilmListView(LoginRequiredMixin, ListView):
    model = Film
    template_name = 'niab_app/film_list.html'  # Renommez ce fichier
    context_object_name = 'films'  # Changez cette variable
    ordering = ['-date']
    paginate_by = 10

class FilmDetailView(LoginRequiredMixin, DetailView):
    model = Film
    template_name = 'niab_app/film_detail.html'  # Renommez ce fichier
    context_object_name = 'film'  # Ajoutez cette ligne