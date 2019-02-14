# Django
from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from parametros.models.menus import Menu

class MenuSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=30, allow_blank=False,validators=[UniqueValidator(queryset=Menu.objects.all())])
    class Meta:
        model = Menu
        fields = ('id', 'nombre')
