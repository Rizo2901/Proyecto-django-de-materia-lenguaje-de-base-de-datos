from django.contrib import admin
from .models import Visitas, Temas , Suscripciones , Usuarios , Subtemas , Autores, Portada ,Noticias ,Envios ,Calificaciones ,CorreosAutomaticos ,Comentarios

admin.site.register(Comentarios)
admin.site.register(Visitas)
admin.site.register(Temas)
admin.site.register(Suscripciones)
admin.site.register(Usuarios)
admin.site.register(Subtemas)
admin.site.register(Autores)
admin.site.register(Portada)
admin.site.register(Noticias)
admin.site.register(Envios)
admin.site.register(Calificaciones)
admin.site.register(CorreosAutomaticos)