from django.shortcuts import render
from django.db.models import Q
from .models import Ejercicio, Subtema
from .forms import BusquedaEjercicioForm

# Create your views here.
def docente(request):
    return render(request, 'docente/homeDocente.html')


def ejercicios(request):
    form = BusquedaEjercicioForm(request.GET or None)

    ejercicios = Ejercicio.objects.all()

    if form.is_valid():
        tema = form.cleaned_data["tema"]
        subtema1 = form.cleaned_data["subtema1"]
        subtema2 = form.cleaned_data["subtema2"]
        momento = form.cleaned_data["momento"]
        nivel = form.cleaned_data["nivel"]
        num_alumnos = request.GET.get('num_alumnos')

        # 🔎 Filtrado obligatorio
        ejercicios = ejercicios.filter(
            tema=tema,
            momento=momento,
            nivel__icontains=nivel,  # ✅ clave para MultiSelectField
        )

        # 🔎 Filtrado opcional
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

    return render(request, "docente/ejercicios.html", {
        "form": form,
        "ejercicios": ejercicios
    })
