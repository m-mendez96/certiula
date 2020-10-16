from django import forms

## Formulario de Creación de Documentos
class DocumentForm(forms.Form):
    descripcion_titulo = forms.CharField(max_length=50,required=False)
    descripcion_notas = forms.CharField(max_length=50,required=False)
    descripcion_acta = forms.CharField(max_length=50,required=False)

