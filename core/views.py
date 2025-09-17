from django.shortcuts import render

# Vistas de la APP core.

def home(request):
    return render(request, 'core/home.html')

