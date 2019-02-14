# standar library

# third.party

# Django
from django.core.validators import RegexValidator
from django.db import models

# Exceptions


validar_nombre = RegexValidator(regex=r'^[A-Za-záéíóúáéíóúÁÉÍÓÚ]+$',
message= ("El nombre no puede estar vacios"))

ERROR_CAMPO_VACIO = 'El campo no puede estar vacio'
ERROR_VALOR_NULO = 'No se admiten valores nulos'

class Menu(models.Model):
    nombre = models.TextField(blank=False, default= '', unique=True,  error_messages={'blank':ERROR_CAMPO_VACIO, 'null': ERROR_VALOR_NULO,  'unique': "Ya existe ese menu"},validators=[validar_nombre])
