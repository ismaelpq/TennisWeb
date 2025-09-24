from django.shortcuts import render

# Create your views here.
def docente(request):
    return render(request, 'docente/homeDocente.html')

def ejercicios(request):
    return render(request, 'docente/ejercicios.html')