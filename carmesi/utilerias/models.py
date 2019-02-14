
# standar library
from django.conf import settings
# Django
from django.db import models
from django_currentuser.middleware import get_current_user


class CarmesiAudit(models.Model):
    """
    Modelo de Auditoria de quien y cuando se modifican los datos del modelo
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Fecha de creación'
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Fecha de actualización'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_creado_por',
        null=True,
        blank=True,
        help_text='Usuario de creación'
    )

    """Creado Por - tipo: ForeignKey"""
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_modificado_por',
        null=True,
        blank=True,
        help_text='Usuario última actualización')

    class Meta:
        abstract = True

    def get_user(self):
        return get_current_user()

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created_by = self.get_user()
        else:
            self.modified_by = self.get_user()
        super(CarmesiAudit, self).save(*args, **kwargs)

