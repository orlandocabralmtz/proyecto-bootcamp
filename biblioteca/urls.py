from django.urls import path
from . import views

urlpatterns = [
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("libros/", views.lista_libros, name="lista_libros"),
    path("prestamos/", views.usuarios_con_libros, name="usuarios_con_libros"),
    path("libros/agregar/", views.agregar_libro, name="agregar_libro"),
    path(
        "eliminar_prestamo/<int:libro_id>/",
        views.eliminar_prestamo,
        name="eliminar_prestamo",
    ),
    path("usuarios_con_libros/", views.usuarios_con_libros, name="usuarios_con_libros"),
    path(
        "eliminar_usuario/<int:usuario_id>/",
        views.eliminar_usuario,
        name="eliminar_usuario",
    ),
    path("eliminar_libro/<int:libro_id>/", views.eliminar_libro, name="eliminar_libro"),
]
