from django.urls import path
from .views import HomePageView, AuthenticationView, CreateClientView, ProfilView, LoanRequestView, BankNewsView, AddNewsView, logout_view, LoanRequestsListView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  


]