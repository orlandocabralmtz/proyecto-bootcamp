from django.shortcuts import render, redirect
from .models import Usuario, Libro
from .forms import LibroForm


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


def agregar_libro(request):
    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el libro en la base de datos
            return redirect("lista_libros")  # Redirige a la lista de libros
    else:
        form = LibroForm()  # Muestra un formulario vacío

    return render(request, "biblioteca/agregar_libro.html", {"form": form})
