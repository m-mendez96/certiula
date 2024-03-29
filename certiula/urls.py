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
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from django.views.generic.base import TemplateView
from apps.user.views import *
from apps.request.views import *
from apps.document.views import *
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    ## Home
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home/index.html'), name="index"),
    path('about/', TemplateView.as_view(template_name='home/about.html'), name="about"),
    path('services/',TemplateView.as_view(template_name='home/services.html'), name = 'services'),
    path('instructives/',TemplateView.as_view(template_name='home/instructives.html'), name = 'instructives'),
    path('contact/',TemplateView.as_view(template_name='home/contact.html'), name = 'contact'),
    ## Inicio de Session
    path('login/',Login.as_view(), name='login'),
    path('session/',login_required(Initial_User.as_view()),name='initial_user'),
    ## Perfil
    path('session/profile/',login_required(Profile.as_view()), name = 'profile'),
    ## Cuenta
    path('session/account/',login_required(Account.as_view()), name = 'account'),
    ## Registro
    path('signup/',Signup, name = 'signup'),
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
    ## Cierre de Sesion
    path('logout/',login_required(LogoutView.as_view()), name='logout'),
    ## Autoridad de Acreditación
    path('session/accreditation_authority/',login_required(Accreditation_Authority.as_view()), name='accreditation_authority'),
    path('session/register/accreditation_authority/',login_required(Register_Accreditation_Authority.as_view()), name='register_accreditation_authority'),
    path('session/register/certification_authority/',login_required(Register_Certification_Authority.as_view()), name='register_certification_authority'),
    path('session/info/certification_authority', login_required(Info_Certification_Authority.as_view()), name='info_certification_authority'),
    ## Autoridad de Certificación
    path('session/certification_authority/',login_required(Certification_Authority.as_view()), name='certification_authority'),
    path('session/register/certifiers/',login_required(Register_Certifiers.as_view()), name='register_certifiers'),
    path('session/certifiers/get/',login_required(Info_Certifiers.as_view()), name='info_certifiers'),
    ## Certificador(es)
    path('session/certifier/',login_required(Certifier.as_view()), name='certifier'),
    ## Crear Solicitud
    path('session/request/documents',login_required(Create_Request.as_view()), name='create_request'),
    ## Obtener Solicitudes
    path('session/requests/get',login_required(Get_Requests.as_view()), name='get_requests'),
    ## Obtener Solicitud
    path('session/request/<int:pk>/get',login_required(Get_Request.as_view()), name='get_request'),
    ## Eliminar Solicitud
    path('session/request/<int:pk>/delete',login_required(Delete_Request.as_view()), name='delete_request'),
    ## Obtener Solcitudes Unidades Funcionales
    path('session/funtional_unit/',login_required(Get_Requests_Functional_Units.as_view()), name='funtional_units'),
    ## Obtener Solcitud Unidades Funcionales
    path('session/funtional_unit/<int:pk>/request/',login_required(Get_Request_Funtional_Units.as_view()), name='get_request_funtional_units'),
    ## Procesar Solcitud Unidades Funcionales
    path('session/funtional_unit/<int:pk>/request/update',login_required(Update_Request_State.as_view()), name='update_request_state'),
    ## Cancelar Solcitud Unidades Funcionales
    path('session/funtional_unit/<int:pk>/request/cancel',login_required(Update_Request_Cancel.as_view()), name='update_request_cancel'),
    ## Crear Documentos de Solicitud
    path('session/funtional_unit/create/documents/<int:request_id>',login_required(Create_Documents.as_view()), name='create_documents'),
    ## Obtener Solicitudes Autoridad de Certificación
    path('session/certification_authority/requests',login_required(Get_Requests_Autoritiy_Certification.as_view()), name='get_requests_autority_certification'),
    ## Obtener Solicitud Autoridad de Certificación
    path('session/certification_authority/<int:pk>/request',login_required(Get_Request_Autority_Certification.as_view()), name='get_request_autority_certification'),
    ## Procesar Solicitud Autoridad de Certificación
    path('session/certification_authority/<int:pk>/request/update',login_required(Update_Request_Autority_Certification.as_view()), name='update_request_autority_certification'),
    ## Obtener Documentos Certificadores
    path('session/certifier/documents/signature',login_required(Get_Documents_Certifiers.as_view()), name='get_documents_certifiers'),
    ## Obtener Documento Certificador
    path('session/certifier/document/<int:pk>',login_required(Get_Document_Certifier.as_view()), name='get_document_certifier'),
    ## Cancelar Documento Certificador
    path('session/certifier/<int:pk>/document/cancel',login_required(Update_Document_Cancel.as_view()), name='update_document_cancel'),
    ## Procesar/Firmar Documento Certificardor
    path('session/certifier/document/<int:pk>/signature/',login_required(Update_Document_Certifier.as_view()), name='update_document_certifier'),
    ## Obtener Documentos a Agregar Dependencia de Certificación
    path('session/certification_authority/documents/add_dependency',login_required(Add_Dependency_Documents.as_view()), name='add_dependency_documents'),
    ## Obtener Documento Autoridad de Certificacion
    path('session/certification_authority/document/<int:pk>', login_required(Get_Document_Authority_Certification.as_view()), name='get_document'),
    ## Agregar Dependencia de Certificación a Documento
    path('session/certification_authority/document/<int:pk>/add_dependency', login_required(Update_Document_Certification_Authority.as_view()), name='update_document_certification_authority'),
    ## Obtener Documentos Beneficiario
    path('session/beneficiary/get/documents/', login_required(Get_Documents_Beneficiary.as_view()), name='get_documents_beneficiary'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Administración de Certiula'
