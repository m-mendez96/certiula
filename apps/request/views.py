from django.views.generic import ListView, View, UpdateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from apps.user.models import *
from .forms import *
from .models import Request

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

## Ver Solicitud
class Get_Request(View):
    def post(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        req = Request.objects.get(request_id=pk)
        return render(request, 'request/get_request.html',{'usuario':usuario, 'user':user,'req':req})

## Eliminar Solicitud
class Delete_Request(View):
    def post(self,request,pk=None,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        Request.objects.filter(request_id=pk).delete()
        return redirect('get_requests')
