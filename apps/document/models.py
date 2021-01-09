from django.db import models
from datetime import datetime
from apps.user.models import UserExtension
from apps.request.models import Request

# Modelo de Documento
class Document(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length = 40, blank=False)
    descripcion = models.CharField(max_length = 70, blank=True)
    STATE = (
        ('F-AC','Firmado AC'),
        ('F-C1','Firmado C1'),
        ('F-C2','Firmado C2'),
        ('C','Cancelado'),
    )
    estado = models.CharField(max_length=4, choices=STATE, default=STATE[0][0])
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
    archivo = models.FileField(upload_to ='documentos/',blank=False,null = False, default='documentos/default.pdf')
    beneficiario = models.ForeignKey(UserExtension, on_delete =models.CASCADE, blank=False)
    request = models.ForeignKey(Request, on_delete =models.CASCADE, blank=False)
    address_blockchain = models.CharField(max_length=64, blank= False, default = " ")
    add_dependencia = models.BooleanField(blank = True, null = True, default = False)
    is_validated = models.BooleanField(blank = True, null = True, default = False)
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return '%s %s %s %s %s' % (self.id,self.titulo,self.categoria,self.tipo_documento,self.beneficiario)