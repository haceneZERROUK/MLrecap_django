from django.urls import path
from .views import DashboardView, HomePageView, MyLoginView, ContactView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import reverse_lazy



urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),  
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  
    path('login/', MyLoginView.as_view(), name='login'),  
    
    path('password_reset/', auth_views.PasswordResetView.as_view(
    template_name='password_reset.html',
    email_template_name='password_reset_email.html',
    subject_template_name='password_reset_subject.txt',
    success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    template_name='password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='password_reset_confirm.html',
    success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    template_name='password_reset_complete.html'
    ), name='password_reset_complete'),

    path("logout/", auth_views.LogoutView.as_view(next_page="homepage"), name="logout"),
    
    path('contact/', ContactView.as_view(), name='contact'),  
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    template_name='password_reset_complete.html'
    ), name='password_reset_complete'),

    
    
]


