# Django
from django.contrib import admin

# Models
from .models import Menu, NodoMenu

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

class NodoMenuAdmin(admin.ModelAdmin):
    list_display = ('id','menu','etiqueta','orden')


admin.site.register(Menu ,MenuAdmin)
admin.site.register(NodoMenu, NodoMenuAdmin)
