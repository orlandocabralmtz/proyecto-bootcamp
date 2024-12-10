from django.urls import path
from . import views

urlpatterns = [
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("libros/", views.lista_libros, name="lista_libros"),
    path("prestamos/", views.usuarios_con_libros, name="usuarios_con_libros"),
]
