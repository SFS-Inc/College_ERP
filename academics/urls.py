from django.urls import path
from . import views

urlpatterns = [
    # --- Faculty Features ---
    path('log/', views.log_engagement, name='log_engagement'),
    path('history/', views.faculty_history, name='faculty_history'),
    
    # FIX: Add this missing line!
    path('delete-log/<int:log_id>/', views.delete_log, name='delete_log'),

    # --- HTMX Endpoints ---
    path('htmx/get-semesters/', views.get_semesters, name='get_semesters'),
    path('htmx/get-batches/', views.get_batches, name='get_batches'),
    path('htmx/get-chapters/', views.get_chapters, name='get_chapters'),
    path('htmx/get-topics/', views.get_topics, name='get_topics'),
    
    # --- Subject Management ---
    path('subjects/', views.manage_subjects, name='manage_subjects'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),

    # --- Admin Panel Features ---
    path('faculty/', views.manage_faculty, name='manage_faculty'),
    path('faculty/add/', views.add_faculty, name='add_faculty'),

    path('batches/', views.manage_batches, name='manage_batches'),
    path('batches/add/', views.add_batch, name='add_batch'),

    path('sessions/', views.manage_sessions, name='manage_sessions'),
    path('sessions/add/', views.add_session, name='add_session'),
    path('sessions/activate/<int:session_id>/', views.activate_session, name='activate_session'),
]