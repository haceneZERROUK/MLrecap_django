from django.shortcuts import render
from django.views.generic import View, ListView, FormView, TemplateView
from .models import Movie


# Create your views here.



class DashboardView(View) : 
    
    template_name = "dashboard.html"
    
    def get(self, request) : 
    
        movies_list = Movie.objects.all()
        context = {"movies_list" : movies_list}
        return render(request, self.template_name, context)
    
    
    def post(self, request) : 
        
        
        pass







