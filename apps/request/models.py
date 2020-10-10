from django.db import models
from datetime import datetime
from apps.user.models import UserExtension

# Modelo de Solicitud de Certificación de Documentos
class Request(models.Model):
    request_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(UserExtension, on_delete =models.CASCADE, blank=False)
    STATE = (
        ('R','Realizada'),
        ('P-UR','Procesada Unidad de Receptoria'),
        ('P-UA','Procesada Unidad de Archivo'),
        ('P-UP','Procesada Unidad de Procesamiento'),
        ('P-CO','Procesada Coordinación'),
        ('P-SE','Procesada Secretaria'),
        ('P-RE','Procesada Rectorado'),
        ('T','Concluida'),
        ('C','Cancelada'),
    )
    estado = models.CharField(max_length=4, choices=STATE, default=STATE[0][0])
    TYPE = (
        ('L','Legalizados'),
        ('C','Certificados'),
    )
    tipo = models.CharField(max_length=1, choices=TYPE, blank=False)
    fecha = models.DateTimeField(default=datetime.now)
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
    facultad_nucleo = models.CharField(max_length=4, choices=FACULTADES_NUCLEOS, blank=False)
    escuela = models.CharField(max_length = 50, blank=False)
    titulo_obtenido = models.CharField(max_length = 50, blank=False)
    fecha_grado = models.DateField(blank=False)
    # Documentos Solicitados
    titulo = models.BooleanField(default=False)
    notas = models.BooleanField(default=False)
    acta = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

    def __str__(self):
        return '%s %s %s %s %s' % (self.request_id,self.usuario,self.estado,self.tipo,self.fecha)