from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# This is the function that was missing!
@login_required
def faculty_dashboard(request):
    return render(request, 'users/dashboard.html')