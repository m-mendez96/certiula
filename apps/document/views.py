from django.shortcuts import render, redirect
from django.views.generic import ListView, View, UpdateView
from apps.user.models import *
from apps.request.models import *
from .models import *

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