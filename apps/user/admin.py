from django.contrib import admin
from .models import *

class UserExtensionAdmin(admin.ModelAdmin):
    search_fields = ['usuario__username','identificacion','usuario__email']
    list_display = ('username','identificacion','first_name','last_name','email',)

    def username(self,x):
        return x.usuario.username
    username.short_description = 'usuario'

    def first_name(self,x):
        return x.usuario.first_name
    first_name.short_description = 'nombre'

    def last_name(self,x):
        return x.usuario.last_name
    last_name.short_description = 'apellido'

    def email(self,x):
        return x.usuario.email
    email.short_description = 'correo electronico'

class FunctionalUnitAdmin(admin.ModelAdmin):
    search_fields = ['usuario__username','usuario__email','unidad_id']
    list_display = ('username','unidad_id',)

    def username(self,x):
        return x.usuario.username
    username.short_description = 'usuario'

class AuthorityAdmin(admin.ModelAdmin):
    search_fields = ['usuario__usuario__username','usuario__usuario__email','tipo','usuario__usuario__first_name','usuario__usuario__last_name',]
    list_display = ('username','tipo','first_name','last_name','email','organizacion_id',)

    def username(self,x):
        return x.usuario.usuario.username
    username.short_description = 'usuario'

    def first_name(self,x):
        return x.usuario.usuario.first_name
    first_name.short_description = 'nombre'

    def last_name(self,x):
        return x.usuario.usuario.last_name
    last_name.short_description = 'apellido'

    def email(self,x):
        return x.usuario.usuario.email
    email.short_description = 'correo electronico'

class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['organizacion_id']
    list_display = ('organizacion_id','nombre',)

admin.site.register(UserExtension,UserExtensionAdmin)
admin.site.register(FunctionalUnit,FunctionalUnitAdmin)
admin.site.register(Authority,AuthorityAdmin)
admin.site.register(Organization,OrganizationAdmin)
