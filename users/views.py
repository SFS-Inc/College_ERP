from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Max # <-- IMPORT THIS!
from academics.models import ClassLog     # <-- IMPORT THIS!

@login_required
def faculty_dashboard(request):
    # Get list of group names for this user (e.g. ['Faculty', 'Faculty_Admin'])
    user_groups = list(request.user.groups.values_list('name', flat=True))
    
    return render(request, 'users/dashboard.html', {
        'user_groups': user_groups
    })

@login_required
def profile(request):
    return render(request, 'users/profile.html') # Dummy page

# --- NEW FUNCTION ---
def is_faculty_admin(user):
    return user.groups.filter(name='Faculty_Admin').exists()

@login_required
@user_passes_test(is_faculty_admin) # Security: Only Admins can see this page!
def admin_menu(request):
    return render(request, 'users/admin_menu.html')



@login_required
def faculty_dashboard(request):
    # 1. Get User Groups (for the Admin Panel card)
    user_groups = list(request.user.groups.values_list('name', flat=True))
    
    # 2. Calculate "Recently Updated" Stats
    # Logic: Group logs by (Subject, Batch), Sum hours, find latest update time.
    recent_stats = ClassLog.objects.filter(faculty=request.user) \
        .values('subject__name', 'batch__name', 'batch__semester__name') \
        .annotate(total_hours=Sum('duration_hours'), last_update=Max('created_at')) \
        .order_by('-last_update')[:4] # Get top 4 most recent
    
    return render(request, 'users/dashboard.html', {
        'user_groups': user_groups,
        'recent_stats': recent_stats
    })