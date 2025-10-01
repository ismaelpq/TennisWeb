from django.shortcuts import render
from django.db.models import Q
from .models import Ejercicio, Tema, Subtema1, Subtema2
from .forms import BusquedaEjercicioForm, BusquedaSimpleForm


# -------------------------
# Home Docente
# -------------------------
def docente(request):
    return render(request, 'docente/homeDocente.html')


# -------------------------
# Ejercicios
# -------------------------
def ejercicios(request):
    # Tomar GET parameters para pasar al form
    tema_id = request.GET.get("advanced-tema")
    subtema1_id = request.GET.get("advanced-subtema1")

    # Formularios
    simple_form = BusquedaSimpleForm(request.GET or None, prefix="simple")
    advanced_form = BusquedaEjercicioForm(
        request.GET or None, 
        prefix="advanced",
        tema_id=tema_id,
        subtema1_id=subtema1_id
    )

    # Query inicial
    ejercicios = Ejercicio.objects.all()

    # --- FILTRO SIMPLE ---
    if simple_form.is_valid() and simple_form.cleaned_data.get("query"):
        q = simple_form.cleaned_data["query"]
        ejercicios = ejercicios.filter(
            Q(tema__nombre__icontains=q) |
            Q(subtema1__nombre__icontains=q) |
            Q(subtema2__nombre__icontains=q) |
            Q(etiquetas__icontains=q)  # corregido, etiquetas es TextField
        ).distinct()

    # --- FILTRO AVANZADO ---
    elif advanced_form.is_valid():
        tema = advanced_form.cleaned_data.get("tema")
        subtema1 = advanced_form.cleaned_data.get("subtema1")
        subtema2 = advanced_form.cleaned_data.get("subtema2")
        momento = advanced_form.cleaned_data.get("momento")
        nivel = advanced_form.cleaned_data.get("nivel")
        sin_raqueta = advanced_form.cleaned_data.get("sin_raqueta")
        num_alumnos = advanced_form.cleaned_data.get("num_alumnos")

        if tema:
            ejercicios = ejercicios.filter(tema=tema)
        if subtema1:
            ejercicios = ejercicios.filter(subtema1=subtema1)
        if subtema2:
            ejercicios = ejercicios.filter(subtema2=subtema2)
        if momento:
            ejercicios = ejercicios.filter(momento=momento)
        if nivel:
            ejercicios = ejercicios.filter(nivel__contains=nivel)
        if num_alumnos:
            try:
                num_alumnos = int(num_alumnos)
                ejercicios = ejercicios.filter(
                    num_alumnos_min__lte=num_alumnos,
                    num_alumnos_max__gte=num_alumnos
                )
            except ValueError:
                pass
        if sin_raqueta:
            ejercicios = ejercicios.filter(sin_raqueta=True)

    return render(request, "docente/ejercicios.html", {
        "simple_form": simple_form,
        "advanced_form": advanced_form,
        "ejercicios": ejercicios
    })



def ejerciciosInfo(request):
    return render(request, 'docente/infoEjercicios.html')


# -------------------------
# Estructuras
# -------------------------
def estructuras(request):
    return render(request, 'docente/estructuras.html')


def estructurasInfo(request):
    return render(request, 'docente/infoEstructuras.html')


# -------------------------
# Generador de Clases
# -------------------------
def generadorClases(request):
    return render(request, 'docente/generadorClases.html')


def generadorClasesInfo(request):
    return render(request, 'docente/infoGenerador.html')
