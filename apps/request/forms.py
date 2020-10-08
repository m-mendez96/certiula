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
class RequestForm(forms.Form):
    tipo = forms.ChoiceField(choices = TYPE, label='Tipo de Documentos Solicitados')
    facultad_nucleo = forms.ChoiceField(choices = FACULTADES_NUCLEOS, label='Facultad o Nucleo')
    escuela = forms.CharField(max_length=50,required=True, label='Escuela')
    titulo_obtenido = forms.CharField(max_length=50,required=True, label='Titulo Obtenido')
    fecha_grado = forms.DateField(required=True, label='Fecha de Grado',input_formats=['dm/%m/%y'])
    #Documentos Solicitados
    titulo = forms.BooleanField(required=False,initial=False,label='Titulo')
    notas = forms.BooleanField(required=False,initial=False,label='Notas')
    acta = forms.BooleanField(required=False,initial=False,label='Acta de Grado')
