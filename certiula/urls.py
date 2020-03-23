"""certiula URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home.as_view(), name = 'index'),
    path('about/',About.as_view(), name = 'about'),
    path('services/',Services.as_view(), name = 'services'),
    path('instructives/',Instructives.as_view(), name = 'instructives'),
    path('contact/',Contact.as_view(), name = 'contact'),
    path('signup/',Signup, name = 'signup'),
    path('password/reset/',PasswordReset, name = 'passwordreset'),
    path('session/',Login, name='login'),
]

admin.site.site_header = 'Administración de Certiula'
