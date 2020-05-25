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
from .models import *
from .forms import *
from .tokens import account_activation_token
import requests

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
        print(w3.eth.accounts[0])
        if user is not None and user.is_active:
            if user.is_superuser:
                return redirect('admin:index')
            if Authority.objects.filter(usuario__usuario = user).exists():
                message = 'Es una Autoridad'
                usuario = UserExtension.objects.get(usuario = self.request.user)
                autoridad = Authority.objects.get(usuario__usuario = user)
                if autoridad.tipo is 'AA':
                    return render(request, 'user/accreditation_authority.html',{'usuario':usuario, 'user':user, 'message':message})
                else:
                    return render(request, 'user/base.html',{'usuario':usuario, 'user':user, 'message':message})
            if FunctionalUnit.objects.filter(usuario = user).exists():
                message = 'Es una Unidad Funcional'
                usuario = None
                return render(request, 'user/base.html',{'usuario':usuario, 'user':user, 'message':message})
            usuario = UserExtension.objects.get(usuario = self.request.user)
            message = 'Es un Usuario'
            return render(request, 'user/base.html',{'usuario':usuario, 'user':user, 'message':message})

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
        return render(request, 'user/profile.html',{'user':user, 'usuario':usuario,'user_form':user_form, 'user_extension_form':user_extension_form})

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
            error_edit = True
            return render(request, 'user/profile.html',{'user':user, 'usuario':usuario,'user_form':user_form, 'user_extension_form':user_extension_form,'error_edit':error_edit})

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
                return render(request, 'user/account.html',{'user':user,'usuario':usuario,'usuario_tipo':usuario_tipo, 'form':form})
            if Authority.objects.filter(usuario__usuario = user).exists():
                usuario = UserExtension.objects.get(usuario = self.request.user)
                usuario_tipo = Authority.objects.get(usuario__usuario = self.request.user)
                return render(request, 'user/account.html',{'user':user,'usuario':usuario,'usuario_tipo':usuario_tipo, 'form':form})
            if UserExtension.objects.filter(usuario = user).exists():
                usuario = UserExtension.objects.get(usuario = self.request.user)
                usuario_tipo = None
            error_change_password = True
            return render(request, 'user/account.html',{'user':user,'usuario':usuario,'usuario_tipo':usuario_tipo, 'form':form, 'error_change_password':error_change_password})


## Registro de Autordiad de Accreditación (MPPES-OPSU)
def Register_Accreditation_Authority(request):
    if request.method == 'POST':
        payload = {
            "owner": "0xeA88D2c82950a0D539438a53387a617327a8e1a3",
            "name": "Boss Enterprises CA",
            "id": 231398,
            "password": "1234567890",
            "email": "boss@example.com" }
        url = "http://127.0.0.1:8080/api/register/accreditation-authority/"
        headers = {}
        response = requests.post(url, data=payload, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            return HttpResponse("Registrada la Autoridad de Accreditación MPPES-OPSU")
        else:
            return redirect('initial_user')
