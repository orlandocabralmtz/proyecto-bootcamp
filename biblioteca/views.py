from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Libro
from .forms import LibroForm


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "biblioteca/lista_usuarios.html", {"usuarios": usuarios})


def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, "biblioteca/lista_libros.html", {"libros": libros})


def usuarios_con_libros(request):
    libros_prestados = Libro.objects.filter(usuario_prestamo__isnull=False)
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


def eliminar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)  # Obtener el libro por su ID
    libro.usuario_prestamo = None  # Eliminar el préstamo (dejar el libro disponible)
    libro.disponible = True  # Establecer 'disponible' en NULL
    libro.save()  # Guardar los cambios en el libro
    return redirect(
        "usuarios_con_libros"
    )  # Redirigir de nuevo a la lista de libros prestados


def usuarios_con_libros(request):
    libros_prestados = Libro.objects.filter(usuario_prestamo__isnull=False)
    usuarios_sin_prestamos = Usuario.objects.filter(libro__isnull=True)
    libros_disponibles = Libro.objects.filter(usuario_prestamo__isnull=True)

    if request.method == "POST":
        # Obtener los datos del formulario
        usuario_id = request.POST.get("usuario")
        libro_id = request.POST.get("libro")

        # Crear el préstamo
        libro = Libro.objects.get(id=libro_id)
        usuario = Usuario.objects.get(id=usuario_id)
        libro.usuario_prestamo = usuario
        libro.disponible = False  # Marcar como no disponible
        libro.save()

        return redirect("usuarios_con_libros")  # Redirigir después de crear el préstamo

    return render(
        request,
        "biblioteca/usuarios_con_libros.html",
        {
            "libros_prestados": libros_prestados,
            "usuarios_sin_prestamos": usuarios_sin_prestamos,
            "libros_disponibles": libros_disponibles,
        },
    )
