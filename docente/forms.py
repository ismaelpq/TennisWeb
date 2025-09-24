from django import forms
from .models import Tema, Subtema, Ejercicio

class BusquedaEjercicioForm(forms.Form):
    tema = forms.ModelChoiceField(
        queryset=Tema.objects.all(),
        required=True,
        label="Tema"
    )
    subtema1 = forms.ModelChoiceField(
        queryset=Subtema.objects.none(),
        required=False,
        label="Subtema 1"
    )
    subtema2 = forms.ModelChoiceField(
        queryset=Subtema.objects.none(),
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

    def __init__(self, *args, **kwargs):
        tema_id = kwargs.pop("tema_id", None)
        super().__init__(*args, **kwargs)

        # Si ya hay un tema elegido, filtra los subtemas
        if tema_id:
            self.fields["subtema1"].queryset = Subtema.objects.filter(tema_id=tema_id)
            self.fields["subtema2"].queryset = Subtema.objects.filter(tema_id=tema_id)
