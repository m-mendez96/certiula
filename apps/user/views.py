from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
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
from .models import UserExtension
from .forms import *
from .tokens import account_activation_token

## Unique email for user
User._meta.get_field('email')._unique = True

## Views home
class Home(ListView):
    def get(self,request,*args,**kwargs):
        return render(request,'home/index.html')

class About(ListView):
    def get(self,request,*args,**kwargs):
        return render(request,'home/about.html')

class Services(ListView):
    def get(self,request,*args,**kwargs):
        return render(request,'home/services.html')

class Instructives(ListView):
    def get(self,request,*args,**kwargs):
        return render(request,'home/instructives.html')

class Contact(ListView):
    def get(self,request,*args,**kwargs):
        return render(request,'home/contact.html')

## Views user
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

def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        if user.is_superuser:
            # Correct password, and the user is marked "is_superuser (Administrador)"
            auth.login(request, user)
            # Redirect to a view admintrator.
            return redirect('admin:index')
        else:
            auth.login(request, user)
            return redirect('index')
    else:
        return HttpResponse('Usuario o Contraseña Invalido o Cuenta Inactiva')
