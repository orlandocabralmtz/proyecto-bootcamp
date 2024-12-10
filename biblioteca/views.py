from django.shortcuts import render
from .models import Usuario, Libro


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "biblioteca/lista_usuarios.html", {"usuarios": usuarios})


def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, "biblioteca/lista_libros.html", {"libros": libros})


def usuarios_con_libros(request):
    libros_prestados = Libro.objects.filter(usuario__isnull=False)
    return render(
        request,
        "biblioteca/usuarios_con_libros.html",
        {"libros_prestados": libros_prestados},
    )
