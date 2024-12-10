from django.db import models


# Definimos la clase Usuario que hereda de models.Model, representando un usuario en la base de datos
class Usuario(models.Model):
    """
    El modelo Usuario representa un usuario en el sistema de biblioteca.Esto quiere decir que los datos
    de los usuarios se guardarán de esta forma en la base de datos.
    Atributos:
        nombre (str): El nombre del usuario.
        email (str): La dirección de correo electrónico del usuario, que debe ser única.
        fecha_registro (datetime): La fecha y hora en que el usuario se registró, automáticamente establecida a la fecha y hora actual.
    Métodos:
        __str__(): Devuelve la representación en cadena del usuario, que es el nombre del usuario.
    """

    # Campo 'nombre' que almacena el nombre del usuario como una cadena de texto con un máximo de 255 caracteres
    nombre = models.CharField(max_length=255)

    # Campo 'email' que almacena la dirección de correo electrónico del usuario, debe ser única en la base de datos
    email = models.EmailField(unique=True)

    # Campo 'fecha_registro' que almacena la fecha y hora en que el usuario se registró, se establece automáticamente al crear una nueva instancia
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Método especial que devuelve una representación en forma de cadena del objeto, en este caso, el nombre del usuario
    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    fecha_publicacion = models.DateField()
    """
    models.ForeignKey(Usuario): Esto indica que usuario_prestamo es un campo de clave foránea que referencia al modelo Usuario. 
    Esto crea una relación de muchos a uno, lo que significa que múltiples instancias del modelo que contiene este campo pueden estar asociadas con una sola instancia de Usuario.
    null=True: Esto permite que el campo usuario_prestamo se establezca en NULL en la base de datos, lo que significa que no es obligatorio que cada registro tenga un valor para este campo.
    blank=True: Esto permite que el campo se deje en blanco en los formularios, lo que significa que no es requerido para la validación del formulario.
    on_delete=models.SET_NULL: Esto especifica el comportamiento cuando la instancia de Usuario referenciada es eliminada. En este caso, establecer on_delete=models.SET_NULL significa que si el Usuario referenciado es eliminado, el campo usuario_prestamo en los registros relacionados se establecerá en NULL en lugar de eliminar los registros relacionados.
    """
    usuario_prestamo = models.ForeignKey(
        Usuario, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.titulo
