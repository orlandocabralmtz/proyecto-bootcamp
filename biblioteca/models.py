from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    fecha_publicacion = models.DateField()
    usuario_prestamo = models.ForeignKey(
        Usuario, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.titulo
