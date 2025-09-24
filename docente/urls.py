from django.urls import path
from . import views

urlpatterns = [
    path('', views.docente, name='homeDocente'),
    path('ejercicios/', views.ejercicios, name='ejercicios')
]
