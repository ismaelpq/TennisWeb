from django.urls import path
from . import views

urlpatterns = [
    path('', views.docente, name='homeDocente'),
    path('ejercicios/', views.ejercicios, name='ejercicios'),
    path('ejercicios/info', views.ejerciciosInfo, name='infoEjercicios'), 

    path('estructuras', views.estructuras, name='estructuras'), 
    path('estructuras/info', views.estructurasInfo, name='estructurasInfo'),

    path('generadorClases/', views.generadorClases, name='generadorClases'),
    path('generadorClases/info', views.generadorClasesInfo, name='generadorClasesInfo')
]
