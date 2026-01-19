from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def log_class(request):
    return render(request, 'engagement/log_class.html')
