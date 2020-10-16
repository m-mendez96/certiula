from django.views.generic import ListView, View, UpdateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from apps.user.models import *
from apps.document.forms import *
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
