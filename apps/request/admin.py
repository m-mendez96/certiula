from django.contrib import admin
from .models import *

class RequestAdmin(admin.ModelAdmin):
    search_fields = ['usuario','estado','tipo','fecha']
    list_display = ('usuario','estado','tipo','fecha',)

admin.site.register(Request,RequestAdmin)
