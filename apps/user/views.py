from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import auth
from django.contrib.auth.models import User
from .models import UserExtension
from .forms import *

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
def Signup(request):
    user_form = None
    user_extension_form = None
    if request.method == "POST":
        user_form = UserForm(request.POST)
        user_extension_form = UserExtensionForm(request.POST)
        if user_form.is_valid():
            return redirect('index')
            #if user_extension_form.is_valid()
        else:
            return render(request, 'user/signup.html',{'user_extension_form':user_extension_form,'user_form':user_form})
        #first_name = request.POST.get('First_name')
        #last_name = request.POST.get('Last_name')
        #id = request.POST.get('Id')
        #phone = request.POST.get('Phone')
        #birth_date = request.POST.get('Birth_date')
        #home_address = request.POST.get('Home_address')
        #email = request.POST.get('Email')
        #username = request.POST.get('Username')
        #password = request.POST.get('Password')
        #password_confirm = request.POST.get('Password_confirm')
        #user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password)
        #user.save()
        #userextension = UserExtension.objects.create(usuario=user,identificacion=id,fecha_nacimiento=birth_date,telefono=phone,direccion=home_address)
        #userextension.save()
        return redirect('index')
    user_form = UserForm
    user_extension_form = UserExtensionForm
    return render(request, 'user/signup.html',{'user_extension_form':user_extension_form,'user_form':user_form})

def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_superuser:
        # Correct password, and the user is marked "is_superuser (Administrador)"
        auth.login(request, user)
        # Redirect to a view admintrator.
        return redirect('admin:index')

def PasswordReset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        return redirect('index')
    else:
        return render(request,'user/passwordreset.html')
