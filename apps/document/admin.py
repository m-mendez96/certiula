from django.contrib import admin
from .models import *

class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['beneficiario']
    list_display = ('id','titulo','categoria','tipo_documento','beneficiario')

admin.site.register(Document,DocumentAdmin)
