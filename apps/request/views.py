from django.views.generic import ListView, View, UpdateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from apps.user.models import *
from apps.document.forms import *
from apps.document.models import *
from django.conf import settings
from .forms import *
from .models import Request
import requests

## Crear Solicitud de Documentos
class Create_Request(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        form = RequestForm
        message = False
        return render(request, 'request/create_request.html',{'usuario':usuario, 'user':user, 'form':form, 'message':message})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        req = Request(usuario=usuario,tipo=request.POST['tipo'],facultad_nucleo=request.POST['facultad_nucleo'],escuela=request.POST['escuela'],titulo_obtenido=request.POST['titulo_obtenido'],fecha_grado=request.POST['fecha_grado'])
        if 'titulo' in request.POST:
            req.titulo = True
        if 'notas' in request.POST:
            req.notas = True
        if 'acta' in request.POST:
            req.acta = True
        req.save()
        form = RequestForm
        message = True
        return render(request, 'request/create_request.html',{'usuario':usuario, 'user':user, 'form':form, 'message':message})

## Obtener Solicitudes
class Get_Requests(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        list_requests = Request.objects.filter(usuario=usuario)
        return render(request, 'request/get_requests.html',{'usuario':usuario, 'user':user,'list_requests':list_requests})

## Ver Solicitud Beneficiario
class Get_Request(View):
    def get(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        req = Request.objects.get(request_id=pk)
        return render(request, 'request/get_request.html',{'usuario':usuario, 'user':user,'req':req})

## Eliminar Solicitud Beneficiario
class Delete_Request(View):
    def post(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        Request.objects.filter(request_id=pk).delete()
        return redirect('get_requests')

## Obtener Solicitudes Unidadades Funcionales
class Get_Requests_Functional_Units(View):
    def get(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = None
        unidad = FunctionalUnit.objects.get(usuario=user)
        if unidad.unidad_id == 'UR':
            list_requests= Request.objects.filter(estado='R')
            return render(request, 'request/receiving_unit.html',{'user':user,'usuario':usuario,'list_requests':list_requests})
        if unidad.unidad_id == 'UA':
            list_requests= Request.objects.filter(estado='P-UR')
            return render(request, 'request/archive_unit.html',{'user':user,'usuario':usuario,'list_requests':list_requests})
        if unidad.unidad_id == 'UP':
            list_requests= Request.objects.filter(estado='P-UA')
            return render(request, 'request/processing_unit.html',{'user':user,'usuario':usuario,'list_requests':list_requests})

## Ver Solicitud Unidad Funcional
class Get_Request_Funtional_Units(View):
    def get(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = None
        req = Request.objects.get(request_id=pk)
        unidad = FunctionalUnit.objects.get(usuario=user)
        return render(request, 'request/get_request_funtional_units.html',{'usuario':usuario, 'user':user,'req':req,'unidad':unidad})

## Procesar Solicitud Unidades Funcionales
class Update_Request_State(View):
    def post(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        unidad = FunctionalUnit.objects.get(usuario=user).unidad_id
        usuario = None
        req = Request.objects.get(request_id=pk)
        if unidad == 'UR':
            req.estado = 'P-UR'
            req.save()
            return redirect('initial_user')
        if unidad == 'UA':
            req.estado = 'P-UA'
            req.save()
            return redirect('initial_user')
        if unidad == 'UP':
            titulo = req.titulo
            notas = req.notas
            acta = req.acta
            form = DocumentForm
            return render(request, 'document/form_create_documents.html',{'usuario':usuario, 'user':user,'req':req,'unidad':unidad,'titulo':titulo,'notas':notas,'acta':acta,'form':form})

## Cancelar Solicitud Unidades Funcionales
class Update_Request_Cancel(View):
    def post(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        req = Request.objects.get(request_id=pk)
        req.estado = 'C'
        req.save()
        return redirect('initial_user')

## Obtener Solicitudes Autoridad de Certificación (Natali)
class Get_Requests_Autoritiy_Certification(View):
    def get(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        list_requests = Request.objects.filter(estado='P-UP')
        return render(request, 'request/get_requests_autority_certification.html',{'usuario':usuario, 'user':user,'list_requests':list_requests})

## Ver Solicitud Autoridad de Certificación
class Get_Request_Autority_Certification(View):
    def get(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        req = Request.objects.get(request_id=pk)
        list_documents = Document.objects.filter(request=req)
        return render(request, 'request/get_request_autority_certifcation.html',{'usuario':usuario, 'user':user,'req':req,'list_documents':list_documents})

## Procesar Solicitud Autoridad de Certificación
class Update_Request_Autority_Certification(View):
    def post(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        req = Request.objects.get(request_id=pk)
        if req.usuario.registro_blockchain is False:
            token = '%s'%request.POST['token'] # Token AC 
            headers = { "Authorization": "Token {}".format(token)}
            payload = {
                'owner': '%s'%req.usuario.cuenta_blockchain,
                'name': '%s'%req.usuario.usuario.first_name+' '+req.usuario.usuario.last_name,
                'id': '%s'%req.usuario.identificacion,
                'id_number':1000+req.request_id,
                'email': '%s'%req.usuario.usuario.email}
            url = f"{settings.CERTSGEN_URL}/api/register/recipient/"
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                req.usuario.registro_blockchain = True
                r = response.json()
                token = '%s'%r['token'] ## Token Beneficiario
                current_site = get_current_site(request)
                mail_subject = 'Registro de Beneficiario'
                message = render_to_string('user/email_register_recipient.html', {
                    'user': req.usuario.usuario,
                    'token':token,
                })
                text_content = strip_tags(message)
                to_email = req.usuario.usuario.email
                email = EmailMultiAlternatives(
                    mail_subject, message, to=[to_email]
                )
                email.attach_alternative(message, "text/html")
                email.send()
        req.estado = 'T'
        req.save()
        return redirect('get_requests_autority_certification')