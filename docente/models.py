from django.db import models
from multiselectfield import MultiSelectField #permite que haya varios grupos en una variable


class Tema(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Subtema(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name="subtemas", blank=True, null=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tema} - {self.nombre}"



class Ejercicio(models.Model):

    #Definicion de las opciones fijas para las variables descriptivas 

    MOMENTO_CHOICES = [
        ('calentamiento', 'Calentamiento'),
        ('carro', 'Ejercicio Base - Carro'),
        ('juego', 'Ejercicio Base - Juego'),
        ('final', 'Juego Final'),
    ]

    #nivel de los jugadores
    NIVEL_CHOICES = [
        ('iniciacion', 'Iniciación'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    #VARIABLES DESCRIPTIVAS

    #Id unico de cada ejercicio
    id = models.AutoField(primary_key=True)  # Django lo crea solo, pero lo dejamos explícito
    
    #Nombre coloquial de cada ejercicio
    nombre = models.CharField(max_length=200)

    #Momento en el que se aplica el ejericicio
    momento = models.CharField(max_length=50, choices=MOMENTO_CHOICES) #se rellena con las opciones predefinidas

    #??
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)
    
    #??
    subtema1 = models.ForeignKey(Subtema, on_delete=models.SET_NULL, null=True, related_name="ejercicios_sub1")
    
    #??
    subtema2 = models.ForeignKey(Subtema, on_delete=models.SET_NULL, null=True, related_name="ejercicios_sub2")


    #texto largo explicando el ejercicio
    descripcion = models.TextField()

    #texto largo, notas para el profesor- Puede estar vacio gracias a blank=True y null=True
    notas_pedagogicas = models.TextField(blank=True, null=True)

    #Numero de jugadores recomendados ¿PUEDE SER UN RANGO?
    #??
    num_alumnos = models.IntegerField(default=1)

    #Desplegable con los niveles predefinidos
    nivel = MultiSelectField(choices=NIVEL_CHOICES, max_choices=3, max_length=50)


    #integer-tiempo estimado en minutos
    duracion = models.IntegerField(help_text="Duración en minutos", blank=True, null=True)

    #Recursos extras necesarios pàra el ejericcio
    recursos = models.CharField(max_length=200, blank=True, null=True)

    #escala dificultad????

    #??
    dificultad_min = models.TextField(blank=True, null=True, help_text="Cómo hacer el ejercicio más difícil")
    dificultad_max = models.TextField(blank=True, null=True, help_text="Cómo hacer el ejercicio más fácil")

    #Imagenes representando el ejercicio en la carpeta 
    #??
    imagen = models.ImageField(upload_to="ejercicios/", blank=True, null=True)

    #enlace de video o referencia externa
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre
