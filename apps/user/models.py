from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Modelo de Extension de Usuario
class UserExtension(models.Model):
    identificacion = models.CharField(primary_key=True, max_length = 10,help_text=("Venezolano (V-), Extranjero (E-), Pasaporte (P-)"),
        validators=[
            RegexValidator(
                regex='^[V|E|P]\-[1-9][0-9]{6,9}$',
                message="""Introduzca una indentificación válida de acuerdo al formato que corresponda (V-, E-, P-).
                Sólo se permite una letra seguida de un guion y los números con una longitud de maximo 8 carácteres."""
        )])
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length = 15)
    direccion = models.CharField(max_length = 150)
    foto_perfil =  models.ImageField ('Foto Perfil', upload_to = 'profile/', blank=True, null = True, default='profile/user.png')
    usuario = models.OneToOneField(User, on_delete =models.CASCADE, blank = False, null = False)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ('usuario',)

    def __str__(self):
        return self.usuario.username

# Modelo de Unidad Funcional
class FunctionalUnit(models.Model):
    UNIT_TYPE = (
        ('UR','Unidad de Receptoria'),
        ('UA','Unidad de Archivo'),
        ('UP','Unidad de Procesamiento')
    )
    # Si se desea tener varias cuentas por unidades funcionales se cambia el primary_key
    # Por ejemplo, en el caso de Varios Transcriptores se cambia para tener varios de la UT.
    unidad_id = models.CharField(primary_key=True, max_length=2, choices=UNIT_TYPE)
    usuario = models.OneToOneField(User,on_delete =models.CASCADE, blank = False)

    class Meta:
        verbose_name = 'Unidad Funcional'
        verbose_name_plural = 'Unidades Funcionales'
        ordering = ('unidad_id',)

    def __str__(self):
        return '%s %s' % (self.unidad_id,self.usuario.username)

# Modelo de Organización
class Organization(models.Model):
    #Identificador de una organizacion son sus siglas ej. OCGRE-ULA, ULA, MPPES, OPSU, etc.
    organizacion_id = models.CharField(primary_key=True,max_length=10)
    nombre = models.CharField(max_length=80,blank=False)

    class Meta:
        verbose_name = 'Organización'
        verbose_name_plural = 'Organizaciones'
        ordering = ('organizacion_id',)

    def __str__(self):
        return self.organizacion_id

# Model de Autoridad
class Authority(models.Model):
    AUTHORITY_TYPE = (
        ('AA','Autoridad de Acreditación'),
        ('AC','Autoridad de Certificación'),
        ('C','Certificador')
    )
    tipo = models.CharField(max_length=2, choices=AUTHORITY_TYPE)
    usuario = models.OneToOneField(UserExtension,on_delete =models.CASCADE, blank = False)
    organizacion_id = models.ForeignKey (Organization, on_delete =models.CASCADE, blank=False)

    class Meta:
        verbose_name = 'Autoridad'
        verbose_name_plural = 'Autoridades'
        ordering = ('tipo',)

    def __str__(self):
        return '%s %s %s %s' % (self.tipo,self.organizacion_id,self.usuario.usuario.first_name,self.usuario.usuario.last_name)
