from django.db import models
from datetime import datetime
from apps.user.models import UserExtension
from apps.request.models import Request

# Modelo de Documento
class Document(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length = 25, blank=False)
    descripcion = models.CharField(max_length = 50, blank=True)
    CATEGORIA = (
        ('T','Titulo'),
        ('N','Notas'),
        ('A','Acta'),
    )
    categoria = models.CharField(max_length=1, choices=CATEGORIA, blank=False)
    TYPE = (
        ('L','Legalizado'),
        ('C','Certificado'),
    )
    tipo_documento = models.CharField(max_length=1, choices=TYPE, blank=False)
    fecha = models.DateTimeField(default=datetime.now)
    beneficiario = models.ForeignKey(UserExtension, on_delete =models.CASCADE, blank=False)
    request = models.ForeignKey(Request, on_delete =models.CASCADE, blank=False)
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return '%s %s %s %s %s' % (self.id,self.titulo,self.categoria,self.tipo_documento,self.beneficiario)