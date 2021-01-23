from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, UpdateView
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from apps.user.models import *
from apps.request.models import *
from django.conf import settings
from .models import *
import requests

## Crear Documentos Solicitados
class Create_Documents(View):
    def post(self,request,request_id=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = None
        req = Request.objects.get(request_id=request_id)
        if req.titulo is True:
            titulo = Document(titulo='Titulo de '+req.titulo_obtenido,descripcion='de '+req.usuario.usuario.first_name+' '+req.usuario.usuario.last_name,categoria='T',tipo_documento=req.tipo,archivo=request.FILES['titulo'],beneficiario=req.usuario,request=req)
            titulo.save()
        if req.notas is True:
            notas = Document(titulo='Notas de '+req.titulo_obtenido,descripcion='de '+req.usuario.usuario.first_name+' '+req.usuario.usuario.last_name,categoria='N',tipo_documento=req.tipo,archivo=request.FILES['notas'],beneficiario=req.usuario,request=req)
            notas.save()
        if req.acta is True:
            acta = Document(titulo='Acta de Grado de '+req.titulo_obtenido,descripcion='de '+req.usuario.usuario.first_name+' '+req.usuario.usuario.last_name,categoria='A',tipo_documento=req.tipo,archivo=request.FILES['acta'],beneficiario=req.usuario,request=req)
            acta.save()
        req.estado = 'P-UP'
        req.save()
        return redirect('initial_user')

## Obtener Documentos Certificadores (Jóse Maria Anderez, Mario Bonucci)
class Get_Documents_Certifiers(View):
    def get(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        autoridad = Authority.objects.get(usuario__usuario = user)
        if usuario.registro_blockchain == True and autoridad.tipo == 'C':
            if user.first_name == "José María":
                ## Cargo Secretaria
                list_documents = Document.objects.filter(request__estado='T', estado ='F-AC')
                return render(request, 'document/get_documents_certifiers.html',{'usuario':usuario, 'user':user,'list_documents':list_documents})
            elif user.first_name == "Mario":
                ## Cargo Rector
                list_documents = Document.objects.filter(request__estado='T', estado='F-C1', tipo_documento='C', add_dependencia=True, is_validated=False)
                return render(request, 'document/get_documents_certifiers.html',{'usuario':usuario, 'user':user,'list_documents':list_documents})
        else:
            return redirect('logout')
            
## Obtener Documento Certificador (Jóse María Anderez, Mario Bonucci)
class Get_Document_Certifier(View):
    def get(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        document = Document.objects.get(id=pk)
        return render(request, 'document/get_document_certifier.html',{'usuario':usuario, 'user':user,'document':document})

## Cancelar Documento Certificador (Jóse María Anderez, Mario Bonucci)
class Update_Document_Cancel(View):
    def post(self,request,pk=None,*args,**kwargs):
        document = Document.objects.get(id=pk)
        document.estado = 'C'
        document.save()
        return redirect('get_documents_certifiers')

## Procesar Solicitud Ceriticadores
class Update_Document_Certifier(View):
    def post(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user) 
        document = Document.objects.get(id=pk)
        if user.first_name == "José María":
            if document.beneficiario.registro_blockchain is True:
                token = '%s'%request.POST['token'] # Token Certifier 
                headers = { "Authorization": "Token {}".format(token)}
                payload = {
                    'recipient_address': '%s'%document.beneficiario.address_blockchain, # Is Address not Account
                    'title': '%s'%document.titulo,
                    'description': '%s'%document.descripcion
                }
                url = f"{settings.CERTSGEN_URL}/api/register/certificate/"
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    document.estado = 'F-C1'
                    r = response.json()
                    document.address_blockchain = '%s'%r['certificate_address'] ## Certificate Addresss
                    document.save()
                    current_site = get_current_site(request)
                    mail_subject = 'Certificado Registrado'
                    message = render_to_string('document/email_register_certificate.html', {
                        'user': document.beneficiario,
                        'certificate_address':'%s'%r['certificate_address'],
                    })
                    text_content = strip_tags(message)
                    to_email = document.beneficiario.usuario.email
                    email = EmailMultiAlternatives(
                        mail_subject, message, to=[to_email]
                    )
                    email.attach_alternative(message, "text/html")
                    email.send()
            return redirect('get_documents_certifiers')
        elif user.first_name == "Mario":
            token = '%s'%request.POST['token'] # Token Certifier 
            headers = { "Authorization": "Token {}".format(token)}
            payload = {
                'certificate_address': '%s'%document.address_blockchain,
                'params': f'P.A. {usuario.usuario.first_name} {usuario.usuario.last_name} RectorULA'
            }
            url = f"{settings.CERTSGEN_URL}/api/add/signature/"
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                document.is_validated == True
                document.save()   
            return redirect('get_documents_certifiers')

## Documentos a Agregar Dependencia (Solo documentos certificados y registrados en la blockchain)
class Add_Dependency_Documents(View):
    def get(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        autoridad = Authority.objects.get(usuario__usuario = user)
        if usuario.registro_blockchain == True and autoridad.tipo == 'AC':
                list_documents = Document.objects.filter(request__estado='T', estado ='F-C1', tipo_documento='C', add_dependencia=False)
                return render(request, 'document/get_documents_add_dependency.html',{'usuario':usuario, 'user':user,'list_documents':list_documents})
        else:
            return redirect('logout')

## Get Documento Autoridad de Certificación
class Get_Document_Authority_Certification(View):
    def get(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        document = Document.objects.get(id=pk)
        return render(request, 'document/get_document.html',{'usuario':usuario, 'user':user,'document':document})


## Agregar Dependencia de Certificación a un Documento
class Update_Document_Certification_Authority(View):
    def post(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user) 
        document = Document.objects.get(id=pk)
        certifier1 = Authority.objects.get(cargo='S')
        certifier2 = Authority.objects.get(cargo='R')
        if document.beneficiario.registro_blockchain is True:
            token = '%s'%request.POST['token'] # Token Authority Certification 
            headers = { "Authorization": "Token {}".format(token)}
            payload = {
                'certificate_address': '%s'%document.address_blockchain, # Is Address not Account
                'from_owner': '%s'%certifier1.usuario.cuenta_blockchain,
                'to_owner': '%s'%certifier2.usuario.cuenta_blockchain
            }
            url = f"{settings.CERTSGEN_URL}/api/add/certifier-dependency/"
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                document.add_dependencia = True
                document.save()
            return redirect('add_dependency_documents')
        return redirect('add_dependency_documents')