from django.urls import path
from .views import (
    dashboard, log_class, get_active_semester, log_history, admin_dashboard,
    admin_faculty, admin_academics, admin_logs, admin_settings
)

urlpatterns = [
    # Dashboard
    path("dashboard/", dashboard, name="dashboard"),
    
    # Admin
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/faculty/", admin_faculty, name="admin_faculty"),
    path("admin/academics/", admin_academics, name="admin_academics"),
    path("admin/logs/", admin_logs, name="admin_logs"),
    path("admin/settings/", admin_settings, name="admin_settings"),

    # Engagement
    path("log-class/", log_class, name="log_class"),
    path("log-history/", log_history, name="log_history"),
    
    # API
    path("api/get-active-semester/", get_active_semester, name="get_active_semester"),
]
