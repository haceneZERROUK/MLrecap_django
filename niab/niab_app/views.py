from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, FormView, TemplateView
from .models import Movie
from dotenv import load_dotenv
import os
import json


# Create your views here.


class DashboardView(View) : 
    
    template_name = "dashboard.html"
    context_object_name = "dashboard"
    
    def get(self, request) : 
        # pour afficher les différents films
        
        movies_list = Movie.objects.all()
        context = {"movies_list" : movies_list}
        return render(request, self.template_name, context)

        
    def post(self, request):
        movie_id = request.POST.get("id")
        movie = get_object_or_404(Movie, id=movie_id)

        if movie.programmed:
            movie.programmation_start_date = date.today()
            movie.programmation_end_date = date.timedelta(today()+7)        # aujourdh'today + 7 jours
        
        movie.save()

        return redirect("dashboard")  







