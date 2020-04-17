from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth import login
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
from .models import *
from .forms import *
from .tokens import account_activation_token

## Unique email for user
User._meta.get_field('email')._unique = True

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

class Login(FormView):
    template_name = 'home/base.html'
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

class Initial_User(ListView):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        if user is not None and user.is_active:
            if user.is_superuser:
                return redirect('admin:index')
            if Authority.objects.filter(usuario__usuario = user).exists():
                message = 'Es una Autoridad'
                usuario = UserExtension.objects.get(usuario = self.request.user)
                return render(request, 'user/base.html',{'usuario':usuario, 'user':user, 'message':message})
            if FunctionalUnit.objects.filter(usuario = user).exists():
                message = 'Es una Unidad Funcional'
                usuario = None
                return render(request, 'user/base.html',{'usuario':usuario, 'user':user, 'message':message})
            usuario = UserExtension.objects.get(usuario = self.request.user)
            message = 'Es un Usuario'
            return render(request, 'user/base.html',{'usuario':usuario, 'user':user, 'message':message})

class Profile(ListView):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.request.user)
        return render(request, 'user/profile.html',{'user':user})
