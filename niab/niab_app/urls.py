from django.urls import path
from .views import DashboardView, HomePageView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),  
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  
    
]


