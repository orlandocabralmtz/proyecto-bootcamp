# Se crea un formulario para la creación de un nuevo libro
from django import forms
from .models import Libro, Usuario

"""
Los forms se usan para recibir ddatos del usuario, validarlos y enviarlos al servidor.
En Django, los formularios se crean utilizando la clase Form o ModelForm.
Un ModelForm es un formulario que se crea a partir de un modelo de Django y se utiliza para crear, actualizar y eliminar instancias de ese modelo.
"""


class LibroForm(forms.ModelForm):
    """
    Un formulario para crear y actualizar instancias de Libro.
    Este formulario se basa en el modelo Libro (de models.py) e incluye los siguientes campos:
    - titulo: El título del libro.
    - autor: El autor del libro.
    - disponible: Un booleano que indica si el libro está disponible.
    - fecha_publicacion: La fecha de publicación del libro.
    """

    class Meta:
        model = Libro
        fields = ["titulo", "autor", "disponible", "fecha_publicacion"]
        # Definimos un diccionario llamado widgets para personalizar los widgets de los campos del formulario
        # En django, un widget es un componente de la interfaz de usuario que se utiliza para mostrar o interactuar con los datos
        widgets = {
            # Personalizamos el campo 'fecha_publicacion' para que use un widget de entrada de texto (TextInput)
            "fecha_publicacion": forms.TextInput(
                # Especificamos los atributos HTML para el widget de entrada de texto
                attrs={
                    # Añadimos la clase CSS  (bootstrap) 'form-control' para estilizar el campo con Bootstrap
                    # el campo fecha_publicacion se verá conforme la clase 'form-control' de Bootstrap
                    "class": "form-control",
                    # Establecemos el atributo 'id' del elemento de entrada a 'fecha_publicacion'
                    # esto le da un ID unico al campo fecha_publicacion
                    "id": "fecha_publicacion",
                }
            ),
        }


class UsuarioForm(forms.ModelForm):
    """
    UsuarioForm es un ModelForm para el modelo Usuario (viene de models.py).
    Este formulario incluye los siguientes campos:
    - nombre: Un campo de entrada de texto con la clase CSS "form-control".
    - email: Un campo de entrada de correo electrónico con la clase CSS "form-control".
        model: El modelo asociado con este formulario, que es Usuario.
        fields: Una lista de campos a incluir en el formulario, que son "nombre" y "email".
        widgets: Un diccionario que especifica widgets personalizados para los campos del formulario.
    """

    class Meta:
        model = Usuario
        fields = ["nombre", "email"]  # Campos definidos en el modelo
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
