from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
path('', views.HomePageView.as_view(), name='home'),
path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
path('movies/', views.FilmListView.as_view(), name='film_list'),
path('movie/int:pk/', views.FilmDetailView.as_view(), name='film_detail'),
path('login/', LoginView.as_view(template_name='niab_app/login.html'), name='login'),
path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]