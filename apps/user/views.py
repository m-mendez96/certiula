from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from web3 import Web3, HTTPProvider
from django.conf import settings
from .models import *
from .forms import *
from .tokens import account_activation_token
import requests
import json

## Web3 Blockchain Localhost
w3 = Web3(HTTPProvider('http://localhost:8545'))

## Unique email for user
User._meta.get_field('email')._unique = True

## Vistas de Usuario

## Activar Cuenta (Registro)
def Activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return render(request, 'registration/confirmation_email.html',{})
    else:
        return render(request, 'registration/invalid_link.html',{})

## Registro
def Signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_extension_form = UserExtensionForm(request.POST)
        if user_form.is_valid() and user_extension_form.is_valid():
            user = user_form.save(commit=False)
            user_extension = user_extension_form.save(commit=False)
            user.is_active = False
            user.save()
            user_extension.usuario = user
            user_extension.save()
            current_site = get_current_site(request)
            mail_subject = 'Activación de la cuenta Certiula'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            text_content = strip_tags(message)
            to_email = user_form.cleaned_data.get('email')
            email = EmailMultiAlternatives(
                        mail_subject, message, to=[to_email]
            )
            email.attach_alternative(message, "text/html")
            email.send()
            return render(request, 'registration/signup_done.html',{})
        else:
            return render(request, 'registration/signup.html',{'user_extension_form':user_extension_form,'user_form':user_form})
    else:
        user_form = UserForm
        user_extension_form = UserExtensionForm
        return render(request, 'registration/signup.html',{'user_extension_form':user_extension_form,'user_form':user_form})

## Inicio de Sesion
class Login(FormView):
    template_name = 'home/index.html'
    form_class = LoginForm
    success_url = reverse_lazy ('initial_user')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch (self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect (self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

    def get_context_data(self, **kwargs):
        invalid_login = True
        kwargs['invalid_login'] = invalid_login
        return kwargs

## Inicial de Usuario
class Initial_User(ListView):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        if user is not None and user.is_active:
            if user.is_superuser:
                return redirect('admin:index')
            if Authority.objects.filter(usuario__usuario = user).exists():
                message = 'Es una Autoridad'
                usuario = UserExtension.objects.get(usuario = self.request.user)
                autoridad = Authority.objects.get(usuario__usuario = user)
                if autoridad.tipo == 'AA':
                    return redirect('accreditation_authority')
                if autoridad.tipo == 'AC':
                    return redirect('certification_authority')
                if autoridad.tipo == 'C':
                    return redirect('certifier')
            if FunctionalUnit.objects.filter(usuario = user).exists():
                message = 'Es una Unidad Funcional'
                usuario = None
                return redirect('funtional_units')
            usuario = UserExtension.objects.get(usuario = self.request.user)
            return redirect('create_request')

## Perfil
class Profile(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        user_form = EditUserForm(instance=request.user)
        user_extension_form = EditUserExtensionForm(instance=request.user.userextension)
        if FunctionalUnit.objects.filter(usuario = user).exists():
            usuario = None
        else:
            usuario = UserExtension.objects.get(usuario = self.request.user)
            if Authority.objects.filter(usuario__usuario = user).exists():
                usuario_tipo = Authority.objects.get(usuario__usuario = self.request.user)
            else:
                usuario_tipo = None
        return render(request, 'user/profile.html',{'user':user, 'usuario':usuario,'usuario_tipo':usuario_tipo,'user_form':user_form, 'user_extension_form':user_extension_form})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        user_form = EditUserForm(request.POST, instance=self.request.user)
        user_extension_form = EditUserExtensionForm(request.POST, request.FILES, instance=self.request.user.userextension)
        if user_form.is_valid() and user_extension_form.is_valid():
            user_form.save()
            user_extension_form.save()
            return redirect('profile')
        else:
            if FunctionalUnit.objects.filter(usuario = user).exists():
                usuario = None
            else:
                usuario = UserExtension.objects.get(usuario = self.request.user)
                if Authority.objects.filter(usuario__usuario = user).exists():
                    usuario_tipo = Authority.objects.get(usuario__usuario = self.request.user)
                else:
                    usuario_tipo = None
            error_edit = True
            return render(request, 'user/profile.html',{'user':user, 'usuario':usuario,'usuario_tipo':usuario_tipo,'user_form':user_form, 'user_extension_form':user_extension_form,'error_edit':error_edit})

## Cuenta
class Account(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        form = PasswordChangeForm(request.user)
        if FunctionalUnit.objects.filter(usuario = user).exists():
            usuario = None
            usuario_tipo = FunctionalUnit.objects.get(usuario = self.request.user)
            return render(request, 'user/account.html',{'user':user,'usuario':usuario,'usuario_tipo':usuario_tipo, 'form':form})
        if Authority.objects.filter(usuario__usuario = user).exists():
            usuario = UserExtension.objects.get(usuario = self.request.user)
            usuario_tipo = Authority.objects.get(usuario__usuario = self.request.user)
            return render(request, 'user/account.html',{'user':user,'usuario':usuario,'usuario_tipo':usuario_tipo, 'form':form})
        if UserExtension.objects.filter(usuario = user).exists():
            usuario = UserExtension.objects.get(usuario = self.request.user)
            usuario_tipo = None
            return render(request, 'user/account.html',{'user':user,'usuario':usuario,'usuario_tipo':usuario_tipo, 'form':form})

    def post(self,request):
        user = User.objects.get(username=self.request.user)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('account')
        else:
            if FunctionalUnit.objects.filter(usuario = user).exists():
                usuario = None
                usuario_tipo = FunctionalUnit.objects.get(usuario = self.request.user)
            if Authority.objects.filter(usuario__usuario = user).exists():
                usuario = UserExtension.objects.get(usuario = self.request.user)
                usuario_tipo = Authority.objects.get(usuario__usuario = self.request.user)
            if UserExtension.objects.filter(usuario = user).exists():
                usuario = UserExtension.objects.get(usuario = self.request.user)
                usuario_tipo = None
            error_change_password = True
            return render(request, 'user/account.html',{'user':user,'usuario':usuario,'usuario_tipo':usuario_tipo, 'form':form, 'error_change_password':error_change_password})

## Autoridad de Acreditacion (MPPES-OPSU - Cesar Trompiz)
class Accreditation_Authority(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        autoridad = Authority.objects.get(usuario__usuario = user)
        if usuario.registro_blockchain == True:
            return render(request, 'user/accreditation_authority.html',{'usuario':usuario, 'user':user})
        else:
            return redirect('register_accreditation_authority')

## Registro de Autoridad de Accreditación (MPPES-OPSU - Cesar Trompiz)
class Register_Accreditation_Authority(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        if usuario.registro_blockchain == False and Authority.objects.get(usuario__usuario = user).tipo == 'AA':
            return render(request, 'user/register_accreditation_authority.html',{'usuario':usuario, 'user':user})
        else:
            return redirect('initial_user')

    def post(self,request):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        payload = {
            'owner': '%s'%request.POST['owner'],
            'name': '%s'%request.POST['name'],
            'id': request.POST['id'],
            'password': '%s'%request.POST['password'],
            'email': '%s'%request.POST['email']}
        url = f"{settings.CERTSGEN_URL}/api/register/accreditation-authority/"
        headers = {}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            usuario = UserExtension.objects.get(usuario = self.request.user)
            usuario.registro_blockchain = True
            usuario.save()
            return render(request, 'user/register_accreditation_authority_done.html',{'usuario':usuario, 'user':user})
        else:
            error_register = True
            response = response.content
            return render(request, 'user/register_accreditation_authority.html',{'usuario':usuario, 'user':user,'error_register':error_register, 'response':response})

## Registro de Autoridad de Certificación (OCGRE-ULA - Natali)
class Register_Certification_Authority(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        autoridad = Authority.objects.get(tipo='AC')
        user_autoridad = User.objects.get(username=autoridad.usuario)
        usuario_autoridad = UserExtension.objects.get(usuario = user_autoridad)
        if usuario.registro_blockchain == True and Authority.objects.get(usuario__usuario = user).tipo == 'AA' and usuario_autoridad.registro_blockchain == False:
            return render(request, 'user/register_certification_authority.html',{'usuario':usuario, 'user':user})
        else:
            return redirect('initial_user')

    def post(self,request):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        payloadAuth = {
            "username": "%s"%request.POST['username'],
	        "password": "%s"%request.POST['password']
        }
        url = f"{settings.CERTSGEN_URL}/api/auth/accreditation-authority/"
        headers = {}
        response = requests.post(url, data=payloadAuth, headers=headers)
        if response.status_code == 200:
            r = response.json()
            token = '%s'%r['token'] ## Token AA
        else:
            token = ' '
        payload = {
        	'owner': '%s'%request.POST['owner'],
        	'name': '%s'%request.POST['name'],
        	'id': request.POST['id'],
        	'email': '%s'%request.POST['email'],
        }
        url = f"{settings.CERTSGEN_URL}/api/register/certification-authority/"
        headers = { "Authorization": "Token {}".format(token)}
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            r = response.json()
            tokenAC = '%s'%r['token'] ## Token AC
            user_registro = User.objects.get(email=request.POST['email'])
            user_extension_registro = UserExtension.objects.get(usuario = user_registro)
            user_extension_registro.registro_blockchain = True
            user_extension_registro.save()
            current_site = get_current_site(request)
            mail_subject = 'Registro de Autoridad de Certificación'
            message = render_to_string('user/email_register_certification_authority.html', {
                'user': user_registro,
                'tokenAC':tokenAC,
            })
            text_content = strip_tags(message)
            to_email = request.POST['email']
            email = EmailMultiAlternatives(
                        mail_subject, message, to=[to_email]
            )
            email.attach_alternative(message, "text/html")
            email.send()
            return render(request, 'user/register_certification_authority_done.html',{'usuario':usuario, 'user':user})
        else:
            error_register = True
            response = response.content
            return render(request, 'user/register_certification_authority.html',{'usuario':usuario, 'user':user,'error_register':error_register, 'response':response})

## Información de Autoridad de Certificación (OCGRE-ULA - Natali)
class Info_Certification_Authority(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        if usuario.registro_blockchain == True and Authority.objects.get(usuario__usuario = user).tipo == 'AA':
            return render(request, 'user/info_certification_authority.html',{'usuario':usuario, 'user':user})
        else:
            return redirect('initial_user')

## Autoridad de Certificación (OCGRE-ULA - Natali)
class Certification_Authority(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        autoridad = Authority.objects.get(usuario__usuario = user)
        if usuario.registro_blockchain == True and autoridad.tipo == 'AC':
            return render(request, 'user/certification_authority.html',{'usuario':usuario, 'user':user})
        else:
            return redirect('logout')

## Registrar Certificadores (Mario Bonucci, José Maria Anderez)
class Register_Certifiers(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        if usuario.registro_blockchain == True and Authority.objects.get(usuario__usuario = user).tipo == 'AC':
            return render(request, 'user/register_certifiers.html',{'usuario':usuario, 'user':user})
        else:
            return redirect('initial_user')
         
    def post(self,request):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        token = '%s'%request.POST['token'] ## Token AC
        headers = { "Authorization": "Token {}".format(token)}
        payload = {
        	'owner': '%s'%request.POST['owner'],
        	'name': '%s'%request.POST['name'],
        	'id_number': request.POST['id'],
            'id':'%s'%request.POST['id_document'],
        	'email': '%s'%request.POST['email'],
        }
        url = f"{settings.CERTSGEN_URL}/api/register/certifier/"
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            r = response.json()
            tokenC = '%s'%r['token'] ## Token Certificador
            user_registro = User.objects.get(email=request.POST['email'])
            user_extension_registro = UserExtension.objects.get(usuario = user_registro)
            user_extension_registro.registro_blockchain = True
            user_extension_registro.save()
            current_site = get_current_site(request)
            mail_subject = 'Registro de Certificador'
            message = render_to_string('user/email_register_certifier.html', {
                'user': user_registro,
                'tokenC':tokenC,
            })
            text_content = strip_tags(message)
            to_email = request.POST['email']
            email = EmailMultiAlternatives(
                        mail_subject, message, to=[to_email]
            )
            email.attach_alternative(message, "text/html")
            email.send()
            payload = {
                'owner': '%s'%request.POST['owner1'],
                'name': '%s'%request.POST['name1'],
                'id_number': request.POST['id1'],
                'id':'%s'%request.POST['id_document1'],
                'email': '%s'%request.POST['email1'],
            }
            url = f"{settings.CERTSGEN_URL}/api/register/certifier/"
            headers = { "Authorization": "Token {}".format(token)}
            response = requests.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                r = response.json()
                tokenC = '%s'%r['token'] ## Token Certificador
                user_registro = User.objects.get(email=request.POST['email1'])
                user_extension_registro = UserExtension.objects.get(usuario = user_registro)
                user_extension_registro.registro_blockchain = True
                user_extension_registro.save()
                current_site = get_current_site(request)
                mail_subject = 'Registro de Certificador'
                message = render_to_string('user/email_register_certifier.html', {
                    'user': user_registro,
                    'tokenC':tokenC,
                })
                text_content = strip_tags(message)
                to_email = request.POST['email1']
                email = EmailMultiAlternatives(
                            mail_subject, message, to=[to_email]
                )
                email.attach_alternative(message, "text/html")
                email.send()
                return render(request, 'user/register_certifiers_done.html',{'usuario':usuario, 'user':user})
        else:
            error_register = True
            response = response.content
            return render(request, 'user/register_certifiers.html',{'usuario':usuario, 'user':user,'error_register':error_register, 'response':response})

## Información de Certificadores (Mario Bonucci, José Maria Anderez)
class Info_Certifiers(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        if usuario.registro_blockchain == True and Authority.objects.get(usuario__usuario = user).tipo == 'AC':
            return render(request, 'user/certifiers.html',{'usuario':usuario, 'user':user})
        else:
            return redirect('initial_user')

## Certificador (Mario Bonucci, José Maria Anderez)
class Certifier(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        usuario = UserExtension.objects.get(usuario = self.request.user)
        autoridad = Authority.objects.get(usuario__usuario = user)
        if usuario.registro_blockchain == True and autoridad.tipo == 'C':
            return redirect('get_documents_certifiers')
        else:
            return redirect('logout')
