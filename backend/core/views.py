from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return HttpResponse("Login successful. Dashboard coming soon.")
