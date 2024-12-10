from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Libro
from .forms import LibroForm, UsuarioForm


def lista_usuarios(request):
    if request.method == "POST":
        # Si se envía el formulario, creamos un nuevo usuario
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario en la base de datos
            return redirect(
                "lista_usuarios"
            )  # Redirigir para evitar reenvíos de formulario
    else:
        form = UsuarioForm()  # Si es un GET, mostramos el formulario vacío

    # Obtener todos los usuarios
    usuarios = Usuario.objects.all()

    return render(
        request, "biblioteca/lista_usuarios.html", {"usuarios": usuarios, "form": form}
    )


def eliminar_usuario(request, usuario_id):
    # Obtener el usuario a eliminar
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Verificar si el usuario tiene algún libro prestado
    libros_prestados = Libro.objects.filter(usuario_prestamo=usuario)

    # Si tiene libros prestados, actualizar el campo disponible
    for libro in libros_prestados:
        libro.disponible = True  # Hacer el libro disponible
        libro.usuario_prestamo = None  # Eliminar la relación de préstamo
        libro.save()

    # Eliminar el usuario
    usuario.delete()

    return redirect("lista_usuarios")  # Redirigir a la lista de usuarios


def lista_libros(request):
    libros = Libro.objects.all()
    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_libros")
    else:
        form = LibroForm()

    return render(
        request, "biblioteca/lista_libros.html", {"libros": libros, "form": form}
    )


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


def eliminar_libro(request, libro_id):
    # Obtener el libro a eliminar
    libro = get_object_or_404(Libro, id=libro_id)

    # Si el libro está prestado, liberar el préstamo
    if libro.usuario_prestamo:
        libro.disponible = True  # Marcar el libro como disponible
        libro.usuario_prestamo = None  # Eliminar el usuario del préstamo
        libro.save()

    # Eliminar el libro
    libro.delete()

    return redirect("lista_libros")  # Redirigir a la lista de libros


# Vista personalizada para el error 404
def pagina_no_encontrada(request, exception):
    return redirect("lista_libros")  # Redirige a la página de lista_libros
