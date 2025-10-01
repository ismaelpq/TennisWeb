from django import forms
from .models import Tema, Ejercicio, Subtema1, Subtema2


# Buscador simple
class BusquedaSimpleForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Buscar tema",
        widget=forms.TextInput(attrs={"placeholder": "Ej: derecha, revés"})
    )


# Buscador avanzado
class BusquedaEjercicioForm(forms.Form):
    tema = forms.ModelChoiceField(
        queryset=Tema.objects.all(),
        required=True,
        label="Tema"
    )
    subtema1 = forms.ModelChoiceField(
        queryset=Subtema1.objects.none(),
        required=False,
        label="Subtema 1"
    )
    subtema2 = forms.ModelChoiceField(
        queryset=Subtema2.objects.none(),
        required=False,
        label="Subtema 2"
    )
    momento = forms.ChoiceField(
        choices=Ejercicio.MOMENTO_CHOICES,
        required=True,
        label="Momento de la clase"
    )
    nivel = forms.ChoiceField(
        choices=Ejercicio.NIVEL_CHOICES,
        required=True,
        label="Nivel"
    )
    num_alumnos = forms.IntegerField(
        required=True,
        label="Número de alumnos (ej: 4)"
    )
    sin_raqueta = forms.BooleanField(
        required=False,
        label="Solo ejercicios sin raqueta"
    )

    def __init__(self, *args, **kwargs):
        # Recibir tema y subtema1 seleccionados para filtrar
        tema_id = kwargs.pop("tema_id", None)
        subtema1_id = kwargs.pop("subtema1_id", None)
        super().__init__(*args, **kwargs)

        if tema_id:
            # Filtrar subtema1 según tema
            self.fields["subtema1"].queryset = Subtema1.objects.filter(tema_id=tema_id)
        if subtema1_id:
            # Filtrar subtema2 según subtema1
            self.fields["subtema2"].queryset = Subtema2.objects.filter(subtema1_id=subtema1_id)
