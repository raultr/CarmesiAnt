# Django
from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


# Mensajes
ERROR_ID_NO_EXISTE = "El {} con el id {} no existe"

class GenericQuerySet(models.query.QuerySet):
    def buscarId(self, id, descripcion):
        try:
            return self.get(id=id)
        except ObjectDoesNotExist:
            raise ValidationError(ERROR_ID_NO_EXISTE.format(descripcion, id))

    def get_filtro(self, **filtros):
        return self.filter(**filtros)
