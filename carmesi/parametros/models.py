from django.db import models

class Menu(models.Model):
    nombre = models.TextField(default= '')

#    def __str__:
#        return self.nombre
