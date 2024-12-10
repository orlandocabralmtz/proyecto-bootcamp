# Se crea un formulario para la creación de un nuevo libro
from django import forms
from .models import Libro


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "autor", "disponible", "fecha_publicacion"]
