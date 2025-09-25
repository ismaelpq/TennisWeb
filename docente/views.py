from django.shortcuts import render
from django.db.models import Q
from .models import Ejercicio, Subtema
from .forms import BusquedaEjercicioForm, BusquedaSimpleForm

# Create your views here.
def docente(request):
    return render(request, 'docente/homeDocente.html')


#Views de apartado Ejercicio ----------------------------------------------------------------------------

def ejercicios(request):
    simple_form = BusquedaSimpleForm(request.GET or None, prefix="simple")
    advanced_form = BusquedaEjercicioForm(request.GET or None, prefix="advanced")

    ejercicios = Ejercicio.objects.all()

    # --- FILTRO SIMPLE ---
    if simple_form.is_valid() and simple_form.cleaned_data.get("query"):
        q = simple_form.cleaned_data["query"]
        ejercicios = ejercicios.filter(
            Q(tema__nombre__icontains=q) |
            Q(subtema1__nombre__icontains=q) |
            Q(subtema2__nombre__icontains=q)
        )

    # --- FILTRO AVANZADO ---
    elif advanced_form.is_valid():
        tema = advanced_form.cleaned_data["tema"]
        subtema1 = advanced_form.cleaned_data["subtema1"]
        subtema2 = advanced_form.cleaned_data["subtema2"]
        momento = advanced_form.cleaned_data["momento"]
        nivel = advanced_form.cleaned_data["nivel"]
        num_alumnos = request.GET.get('advanced-num_alumnos')  # cuidado con prefix

        ejercicios = ejercicios.filter(
            tema=tema,
            momento=momento,
            nivel=nivel,
        )
        if subtema1:
            ejercicios = ejercicios.filter(subtema1=subtema1)
        if subtema2:
            ejercicios = ejercicios.filter(subtema2=subtema2)
        if num_alumnos:
            try:
                num_alumnos = int(num_alumnos)
                ejercicios = ejercicios.filter(
                    num_alumnos_min__lte=num_alumnos,
                    num_alumnos_max__gte=num_alumnos
                )
            except ValueError:
                pass
        if sin_raqueta:  # Aplica filtro si se marcó la casilla
            ejercicios = ejercicios.filter(sin_raqueta=True)

    return render(request, "docente/ejercicios.html", {
        "simple_form": simple_form,
        "advanced_form": advanced_form,
        "ejercicios": ejercicios
    })


def ejerciciosInfo(request):
    return render(request, 'docente/infoEjercicios.html')

# Views sobre estructuras de clases ------------------------------------------------------------------------

def estructuras(request):
    return render(request, 'docente/estructuras.html')


def estructurasInfo(request):
    return render(request, 'docente/infoEstructuras.html')



# Views sobre el generador de clases ------------------------------------------------------------------------

def generadorClases(request):
    return render(request, 'docente/generadorClases.html')


def generadorClasesInfo(request):
    return render(request, 'docente/infoGenerador.html')


