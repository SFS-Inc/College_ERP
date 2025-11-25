from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_engagement, name='log_engagement'),

    # HTMX Endpoints (The Chain)
    path('htmx/get-semesters/', views.get_semesters, name='get_semesters'),
    path('htmx/get-batches/', views.get_batches, name='get_batches'),
    
    # NEW Endpoints
    path('htmx/get-chapters/', views.get_chapters, name='get_chapters'),
    path('htmx/get-topics/', views.get_topics, name='get_topics'),
    
    path('history/', views.faculty_history, name='faculty_history'),

    # Subject Management
    path('subjects/', views.manage_subjects, name='manage_subjects'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
]