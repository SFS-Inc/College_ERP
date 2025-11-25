from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Access this via http://127.0.0.1:8000/login/
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # Access this via http://127.0.0.1:8000/logout/
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('dashboard/', views.faculty_dashboard, name='faculty_dashboard'),


]