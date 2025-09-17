from django.urls import path
from . import views

urlpatterns = [
    path('', views.docente, name='homeDocente')
]
