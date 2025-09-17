from django.urls import path
from . import views

urlpatterns = [
    path('', views.alumno, name='homeAlumno')
]
