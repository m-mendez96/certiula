from django import forms
from .models import *

TYPE = (
    ('L','Legalizados'),
    ('C','Certificados'),
)

FACULTADES_NUCLEOS = (
        ('FAD','Facultad de Arquitectura y Diseño'),
        ('FA','Facultad de Arte'),
        ('FC','Facultad de Ciencias'),
        ('FCES','Facultad de Ciencias Económicas y Sociales'),
        ('FCFA','Facultad de Ciencias Forestales y Ambientales'),
        ('FCJP','Facultad de Ciencias Jurídicas y Políticas'),
        ('FFB','Facultad de Farmacia y Bioanálisis'),
        ('FH','Facultad de Humanidades y Educación'),
        ('FI','Facultad de Ingeniería'),
        ('FM','Facultad de Medicina'),
        ('FO','Facultad de Odontología'),
        ('NURR','Núcleo Universitario Rafael Rangel - Trujillo'),
        ('NUPR','Núcleo Universitario Pedro Rincon Gutierrez - Tachira'),
        ('NUVM','Núcleo Universitario Valle del Mocotíes - Tovar'),
        ('NUAA','Núcleo Universitario Alberto Adriani - El Vigia'),
    )

## Formulario de Solicitud
class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['tipo','facultad_nucleo','escuela','titulo_obtenido','fecha_grado','titulo', 'notas', 'acta']
        widgets = {
            'escuela':forms.TextInput(attrs={'placeholder': 'ej. Sistemas'}),
            'titulo_obtenido':forms.TextInput(attrs={'placeholder': 'ej. Ing. de Sistemas'}),
            'fecha_grado':forms.TextInput(attrs={'placeholder': 'ej. 2010-12-10'}),
        }

