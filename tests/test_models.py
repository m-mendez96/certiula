from django.test import TestCase
from apps.user.models import *
from apps.request.models import *
from apps.document.models import *

class ModelsTestCase(TestCase):
    
    def test_UserExtension(self):
        user = User.objects.create(email="mendezmilena25@gmail.com")
        user.first_name = "Ana"
        user.last_name = "Mendez"
        user.save()
        usuario = UserExtension.objects.create(identificacion="V-16906659", fecha_nacimiento="1986-05-25", usuario=user)
        usuario.save()
        self.assertEqual(user.email, usuario.usuario.email)

    def test_FunctionalUnit(self):
        user_UR = User.objects.create(email="unidad-receptoria@gmail.com")
        user_UR.first_name = "Unidad"
        user_UR.last_name = "Receptoria"
        user_UR.username = "unidad-receptoria"
        user_UR.save()
        unidad_receptoria = FunctionalUnit.objects.create(unidad_id='UR', usuario=user_UR)
        unidad_receptoria.save()
        self.assertEqual(user_UR, unidad_receptoria.usuario)

        user_UA = User.objects.create(email="unidad-archivo@gmail.com")
        user_UA.first_name = "Unidad"
        user_UA.last_name = "Archivo"
        user_UA.username = "unidad-archivo"
        user_UA.save()
        unidad_archivo = FunctionalUnit.objects.create(unidad_id='UA', usuario=user_UA)
        unidad_archivo.save()
        self.assertEqual(user_UA, unidad_archivo.usuario)

        user_UP = User.objects.create(email="unidad-procesamiento@gmail.com")
        user_UP.first_name = "Unidad"
        user_UP.last_name = "Procesamiento"
        user_UP.username = "unidad-procesamiento"
        user_UP.save()
        unidad_procesamiento = FunctionalUnit.objects.create(unidad_id='UP', usuario=user_UP)
        unidad_procesamiento.save()
        self.assertEqual(user_UP, unidad_procesamiento.usuario)

    def test_Organization(self):
        organizacion = Organization.objects.create(organizacion_id="ULA")
        organizacion.nombre = "Universidad de Los Andes"
        organizacion.save()

        organizacion_get = Organization.objects.get(pk="ULA")
        self.assertEqual(organizacion, organizacion_get)

    def test_Authority(self):
        user = User.objects.create(email="jm.ocgre@gmail.com")
        user.first_name = "Cetificador"
        user.last_name = "Secretario"
        usuario = UserExtension.objects.create(identificacion="V-10876539", fecha_nacimiento="1961-10-15", usuario=user)
        organizacion = Organization.objects.create(organizacion_id="ULA")
        organizacion.nombre = "Universidad de Los Andes"
        certificador_secretatio = Authority.objects.create(tipo="C", usuario=usuario,organizacion_id=organizacion)
        certificador_secretatio.save()
        self.assertEqual(usuario, certificador_secretatio.usuario)

    def test_Request(self):
        user = User.objects.create(email="juanlopez@gmail.com")
        user.first_name = "Juan"
        user.last_name = "Lopez"
        usuario = UserExtension.objects.create(identificacion="V-15347985", fecha_nacimiento="1998-10-12", usuario=user)
        request = Request.objects.create(usuario=usuario, estado="R", tipo="C", fecha_grado="2019-07-18")
        request.save()
        self.assertEqual(usuario, request.usuario)

    def test_Document(self):
        user = User.objects.create(email="juanlopez@gmail.com")
        user.first_name = "Juan"
        user.last_name = "Lopez"
        usuario = UserExtension.objects.create(identificacion="V-15347985", fecha_nacimiento="1998-10-12", usuario=user)
        request = Request.objects.create(usuario=usuario, estado="R", tipo="C", fecha_grado="2019-07-18")
        document = Document.objects.create(beneficiario=usuario, request=request, titulo="Documento Certificado")
        document.save()
        self.assertEqual(usuario, document.beneficiario)