from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, UpdateView
from apps.user.models import *
from apps.request.models import *
from .models import *
import requests

## Crear Documentos Solicitados
class Create_Documents(View):
    def post(self,request,request_id=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = None
        req = Request.objects.get(request_id=request_id)
        if req.titulo is True:
            titulo = Document(titulo='Titulo de '+req.titulo_obtenido,descripcion='Titulo de '+req.titulo_obtenido+ ' de '+req.usuario.usuario.first_name+' '+req.usuario.usuario.last_name,categoria='T',tipo_documento=req.tipo,archivo=request.FILES['titulo'],beneficiario=req.usuario,request=req)
            titulo.save()
        if req.notas is True:
            notas = Document(titulo='Notas de '+req.titulo_obtenido,descripcion='Notas de '+req.titulo_obtenido+ ' de '+req.usuario.usuario.first_name+' '+req.usuario.usuario.last_name,categoria='N',tipo_documento=req.tipo,archivo=request.FILES['notas'],beneficiario=req.usuario,request=req)
            notas.save()
        if req.acta is True:
            acta = Document(titulo='Acta de Grado de '+req.titulo_obtenido,descripcion='Acta de Grado de '+req.titulo_obtenido+ ' de '+req.usuario.usuario.first_name+' '+req.usuario.usuario.last_name,categoria='A',tipo_documento=req.tipo,archivo=request.FILES['acta'],beneficiario=req.usuario,request=req)
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
                list_documents = Document.objects.filter(request__estado='T', estado='F-C1', tipo_documento='C')
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

## Procesar Solicitud Autoridad de Certificación
class Update_Document_Certifier(View):
    def post(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user) 
        document = Document.objects.get(id=pk)
        if usuario.registro_blockchain is True:
            token = '%s'%request.POST['token'] # Token Certifier 
            headers = { "Authorization": "Token {}".format(token)}
            payload = {
	            'recipient_address': '0x5A6fc1A1Ffe396567351D9828D9F4e0E109cce5a', # Is Address not Account
                'title': 'Titulo de Ing',
                'description': 'Description of Document'
            }
            url = "http://127.0.0.1:8080/api/register/certificate/"
            print(payload,headers)
            response = requests.post(url, json=payload, headers=headers)
            print(response.content)
            if response.status_code == 200:
                document.estado = 'F-C1'
                r = response.json()
                token = '%s'%r['token'] ## Token Certificado # Here is not funtional
                current_site = get_current_site(request)
                mail_subject = 'Certificado Registrado'
                message = render_to_string('document/email_register_certificate.html', {
                    'user': document.beneficiario,
                    'token':token,
                })
                text_content = strip_tags(message)
                to_email = req.usuario.usuario.email
                email = EmailMultiAlternatives(
                    mail_subject, message, to=[to_email]
                )
                email.attach_alternative(message, "text/html")
                email.send()
        document.save()
        return redirect('get_documents_certifiers')