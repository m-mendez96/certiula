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
from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views
from django.views.generic.base import TemplateView
from apps.user.views import *

urlpatterns = [
    ## Home
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home/index.html'), name="index"),
    path('about/', TemplateView.as_view(template_name='home/about.html'), name="about"),
    path('services/',TemplateView.as_view(template_name='home/services.html'), name = 'services'),
    path('instructives/',TemplateView.as_view(template_name='home/instructives.html'), name = 'instructives'),
    path('contact/',TemplateView.as_view(template_name='home/contact.html'), name = 'contact'),
    ## Registration
    path('signup/',Signup, name = 'signup'),
    path('session/',Login, name='login'),
    path('activate/<uidb64>/<token>/',Activate, name='activate'),
    path('password/reset/',views.PasswordResetView.as_view(html_email_template_name='registration/password_reset_html_email.html'),
        {'template_name':'registration/password_reset_form.html'}, name='password_reset'),
    path('password/reset/done/',views.PasswordResetDoneView.as_view(),
        {'template_name':'registration/password_reset_done.html'}, name='password_reset_done'),
    re_path('password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.PasswordResetConfirmView.as_view(),
        {'template_name' : 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    path('password/reset/complete/', views.PasswordResetCompleteView.as_view(),
        {'template_name' : 'registration/password_reset_complete.html'}, name='password_reset_complete'),
]

admin.site.site_header = 'Administración de Certiula'
