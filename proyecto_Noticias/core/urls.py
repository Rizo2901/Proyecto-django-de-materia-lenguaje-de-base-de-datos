from django.urls import path
from . import views

urlpatterns = [
    path('internacional/', views.internacional_view, name='internacional'),
    path('usuarios/', views.usuarios_view, name='usuarios'),
    path('noticias/', views.noticias_view, name='noticias'),
    path('temas/', views.temas_view, name='temas'),
     path('subtemas/', views.subtemas_view, name='subtemas'),
      path('autores/', views.autores_view, name='autores'),
   
]
