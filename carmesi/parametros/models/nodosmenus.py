# standar library
import json
import copy

# third.party
from sequences import get_next_value

# Django
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import transaction
from django.db.models import F

# Models
from .menus import Menu

#Managers
from parametros.managers.nodosmenus import NodoMenuManager

# Exceptions


ERROR_LONGITUD = "La longitud maxima es de %(limit_value)d caracteres (tiene %(show_value)d)"
ERROR_VALOR_MINIMO = "No se puede mover a un orden menor a 0"



class NodoMenu(models.Model):
    id = models.IntegerField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    nodo_padre = models.ForeignKey('self', null=True, blank=True, related_name='subnodomenu', on_delete=models.PROTECT)
    etiqueta = models.CharField(max_length=60,
        error_messages={'max_length': ERROR_LONGITUD})
    orden = models.PositiveIntegerField(validators=[MinValueValidator(0)],
        error_messages={'min_value': ERROR_VALOR_MINIMO})

    @property
    def id_nodo_padre(self):
        return None if self.nodo_padre == None else self.nodo_padre.id


    #objects = NodoMenuQuerySet.as_manager()
    objects = NodoMenuManager()
