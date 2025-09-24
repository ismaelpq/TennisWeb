from django.shortcuts import render
from .models import Ejercicio
from django.db.models import Q

# Create your views here.
def docente(request):
    return render(request, 'docente/homeDocente.html')

def ejercicios(request):
    return render(request, 'docente/ejercicios.html')



def ejercicios(request):
    query = request.GET.get("q")  # lo que escribe el usuario en el buscador
    ejercicios = Ejercicio.objects.all()  # traemos todos por defecto

    if query:
        ejercicios = ejercicios.filter(
            Q(nombre__icontains=query) |                   # nombre coloquial
            Q(momento__icontains=query) |                  # momento del ejercicio
            Q(tema__nombre__icontains=query) |             # tema (por nombre)
            Q(subtema1__nombre__icontains=query) |         # subtema1
            Q(subtema2__nombre__icontains=query) |         # subtema2
            Q(nivel__icontains=query)                      # nivel de jugadores
        ).distinct()  # evita duplicados si coincide en varios campos

    return render(request, "docente/ejercicios.html", {"ejercicios": ejercicios})
   

