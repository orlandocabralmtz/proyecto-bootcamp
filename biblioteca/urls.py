from django.urls import path
from django.contrib.auth import (
    views as auth_views,
)  # Importamos las vistas de autenticación de Django


"""
Configuración de URLs para el proyecto biblioteca.
La lista `urlpatterns` enruta URLs a vistas. 
Funciones:
    handler404: Manejador personalizado para errores 404, redirige a la vista 'pagina_no_encontrada'.
    urlpatterns: Lista de patrones de URL y sus vistas correspondientes.
Patrones de URL:
    - "usuarios/": Mapea a la vista 'lista_usuarios', muestra una lista de usuarios.
    - "libros/": Mapea a la vista 'lista_libros', muestra una lista de libros.
    - "prestamos/": Mapea a la vista 'usuarios_con_libros', muestra usuarios con libros prestados.
    - "libros/agregar/": Mapea a la vista 'agregar_libro', permite agregar un nuevo libro.
    - "eliminar_prestamo/<int:libro_id>/": Mapea a la vista 'eliminar_prestamo', permite eliminar un préstamo por ID de libro.
    - "usuarios_con_libros/": Mapea a la vista 'usuarios_con_libros', muestra usuarios con libros prestados.
    - "eliminar_usuario/<int:usuario_id>/": Mapea a la vista 'eliminar_usuario', permite eliminar un usuario por ID de usuario.
    - "eliminar_libro/<int:libro_id>/": Mapea a la vista 'eliminar_libro', permite eliminar un libro por ID de libro.
"""
from . import views

# Redirige los errores 404 a la vista personalizada
handler404 = "biblioteca.views.pagina_no_encontrada"  # Esto asegura que cuando ocurra un 404, se redirija a lista_libros

urlpatterns = [
    # Ruta para la lista de usuarios, mapeada a la vista 'lista_usuarios.html'
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    # Ruta para la lista de libros, mapeada a la vista 'lista_libros'
    # Asegúrate de que esta ruta esté aquí
    path("libros/", views.lista_libros, name="lista_libros"),
    # Ruta para la lista de préstamos, mapeada a la vista 'usuarios_con_libros'
    path("prestamos/", views.usuarios_con_libros, name="usuarios_con_libros"),
    # Ruta para agregar un libro, mapeada a la vista 'agregar_libro'
    path("libros/agregar/", views.agregar_libro, name="agregar_libro"),
    # Ruta para eliminar un préstamo, mapeada a la vista 'eliminar_prestamo'
    # La URL incluye un parámetro 'libro_id' que se pasa a la vista
    # Establece un mapeo entre la ruta y la vista (funcion) 'eliminar_prestamo'
    path(
        "eliminar_prestamo/<int:libro_id>/",
        views.eliminar_prestamo,
        name="eliminar_prestamo",
    ),
    # Ruta duplicada para la lista de préstamos, mapeada a la vista 'usuarios_con_libros'
    path("usuarios_con_libros/", views.usuarios_con_libros, name="usuarios_con_libros"),
    # Ruta para eliminar un usuario, mapeada a la vista 'eliminar_usuario'
    # La URL incluye un parámetro 'usuario_id' que se pasa a la vista
    path(
        "eliminar_usuario/<int:usuario_id>/",
        views.eliminar_usuario,
        name="eliminar_usuario",
    ),
    # Ruta para eliminar un libro, mapeada a la vista 'eliminar_libro'
    # La URL incluye un parámetro 'libro_id' que se pasa a la vista
    path("eliminar_libro/<int:libro_id>/", views.eliminar_libro, name="eliminar_libro"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
]
