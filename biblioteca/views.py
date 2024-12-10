from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Libro
from .forms import LibroForm, UsuarioForm


def lista_usuarios(request):
    """
    Maneja la visualización y creación de usuarios.
    Si el método de la solicitud es POST, procesa el formulario enviado para crear un nuevo usuario.
    Si el formulario es válido, el nuevo usuario se guarda en la base de datos y el usuario es redirigido
    a la vista 'lista_usuarios' para evitar el reenvío del formulario.
    Si el método de la solicitud es GET, muestra un formulario vacío para crear un nuevo usuario.
    Además, recupera todos los usuarios de la base de datos y los muestra en la plantilla
    'biblioteca/lista_usuarios.html' junto con el formulario.
    Args:
        request (HttpRequest): El objeto de la solicitud HTTP.
    Returns:
        HttpResponse: La plantilla 'lista_usuarios' renderizada con la lista de usuarios y el formulario.
    """
    if request.method == "POST":
        # Si se envía el formulario (método POST), creamos un nuevo usuario
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guardamos el nuevo usuario en la base de datos
            form.save()
            return redirect("lista_usuarios")
            # Redirigimos a la lista de usuarios para evitar reenvíos de formulario

    else:
        # Si el método de la solicitud es GET, mostramos el formulario vacío
        form = UsuarioForm()

    # Obtener todos los usuarios de la base de datos
    usuarios = Usuario.objects.all()

    # Renderizamos la plantilla 'lista_usuarios.html' con los usuarios y el formulario
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

    """
    Esta vista maneja la visualización y creación de libros.
    Si la solicitud es un método POST, se procesa el formulario para crear un nuevo libro.
    Si la solicitud es un método GET, se muestra un formulario vacío.
    Finalmente, se renderiza la plantilla lista_libros.html con la lista de libros y el formulario.
    """


def lista_libros(request):
    # Obtener todos los libros de la base de datos
    libros = Libro.objects.all()
    if request.method == "POST":
        # Si se envía el formulario (método POST), creamos un nuevo libro
        form = LibroForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guardamos el nuevo libro en la base de datos
            form.save()
            return redirect("lista_libros")
            # Redirigimos a la lista de libros para evitar reenvíos de formulario
    else:
        # Si el método de la solicitud es GET, mostramos el formulario vacío
        form = LibroForm()

    # Renderizamos la plantilla 'lista_libros.html' con los libros y el formulario
    return render(
        request, "biblioteca/lista_libros.html", {"libros": libros, "form": form}
    )


"""
Esta vista maneja la visualización de los libros que están prestados. 
Filtra los libros que tienen un usuario asociado (usuario_prestamo no es nulo) 
y renderiza la plantilla usuarios_con_libros.html con la lista de libros prestados.
"""


def usuarios_con_libros(request):
    # Obtener todos los libros que están prestados (usuario_prestamo no es nulo)
    libros_prestados = Libro.objects.filter(usuario_prestamo__isnull=False)
    # Renderizamos la plantilla 'usuarios_con_libros.html' con los libros prestados
    return render(
        request,
        "biblioteca/usuarios_con_libros.html",
        {"libros_prestados": libros_prestados},
    )


"""
Esta vista maneja la creación de un nuevo libro.
Si la solicitud es un método POST, se procesa el formulario para crear el libro. 
Si la solicitud es un método GET, se muestra un formulario vacío. 
Finalmente, se renderiza la plantilla agregar_libro.html con el formulario.
"""


def agregar_libro(request):
    if request.method == "POST":
        # Si se envía el formulario (método POST), creamos un nuevo libro
        form = LibroForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guardamos el nuevo libro en la base de datos
            form.save()
            return redirect("lista_libros")
            # Redirigimos a la lista de libros para evitar reenvíos de formulario
    else:
        # Si el método de la solicitud es GET, mostramos el formulario vacío
        # Crear una instancia del formulario LibroForm vacío para que pueda ser llenado por el usuario
        form = LibroForm()

    # Renderizamos la plantilla 'agregar_libro.html' con el formulario
    return render(request, "biblioteca/agregar_libro.html", {"form": form})


"""
Esta vista maneja la eliminación de un préstamo. 
Obtiene el libro por su ID, elimina el préstamo (estableciendo usuario_prestamo a None y disponible a True), guarda los cambios y redirige a la lista de libros prestados.
"""


def eliminar_prestamo(request, libro_id):
    # Obtener el libro por su ID
    # get_object_or_404() obtiene un objeto de un modelo o muestra un error 404 si no se encuentra
    libro = get_object_or_404(Libro, id=libro_id)
    # Eliminar el préstamo (dejar el libro disponible)
    libro.usuario_prestamo = None
    libro.disponible = True
    # Guardar los cambios en el libro
    libro.save()
    # Redirigir de nuevo a la lista de libros prestados
    return redirect("usuarios_con_libros")


def usuarios_con_libros(request):
    # Obtener todos los libros que están prestados (usuario_prestamo no es nulo)
    libros_prestados = Libro.objects.filter(usuario_prestamo__isnull=False)
    # Obtener todos los usuarios que no tienen préstamos
    usuarios_sin_prestamos = Usuario.objects.filter(libro__isnull=True)
    # Obtener todos los libros que están disponibles (usuario_prestamo es nulo)
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

        # Redirigir después de crear el préstamo
        return redirect("usuarios_con_libros")

    # Renderizamos la plantilla 'usuarios_con_libros.html' con los datos necesarios
    return render(
        request,
        "biblioteca/usuarios_con_libros.html",
        {
            "libros_prestados": libros_prestados,
            "usuarios_sin_prestamos": usuarios_sin_prestamos,
            "libros_disponibles": libros_disponibles,
        },
    )


""" 
Esta vista maneja la eliminación de un libro. 
Obtiene el libro por su ID, libera el préstamo si el libro está prestado, 
elimina el libro y redirige a la lista de libros.
"""


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

    # Redirigir a la lista de libros
    return redirect("lista_libros")


"""
Esta vista personalizada maneja el error 404 redirigiendo a la página de lista de libros.
"""


# Vista personalizada para el error 404
def pagina_no_encontrada(request, exception):
    # Redirige a la página de lista_libros
    return redirect("lista_libros")
