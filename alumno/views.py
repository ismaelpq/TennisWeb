from django.shortcuts import render

# Create your views here.

def alumno(request):
    return render(request, 'alumno/homeAlumno.html')
