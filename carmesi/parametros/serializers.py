# Django
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueValidator

# Models
from parametros.models import Menu, NodoMenu, ERROR_LONGITUD

class MenuSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=30, allow_blank=False,validators=[UniqueValidator(queryset=Menu.objects.all())])
    class Meta:
        model = Menu
        fields = ('id', 'nombre')


class NodoMenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required= False)
    nodo_padre = serializers.PrimaryKeyRelatedField( allow_null=True, read_only=True)

    class Meta:
        model = NodoMenu
        extra_kwargs = {"etiqueta": {"error_messages": {"max_length":ERROR_LONGITUD}}}
        fields  = ('id','menu','nodo_padre','etiqueta','orden',)



class NodoMenuUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required= False)

    nodo_padre = serializers.PrimaryKeyRelatedField( allow_null=True, read_only=True)

    menu = serializers.IntegerField(required= False)
    orden = serializers.IntegerField(required=False)

    class Meta:
        model = NodoMenu
        extra_kwargs = {"etiqueta": {"error_messages": {"max_length":ERROR_LONGITUD}}}
        fields  = ('id','menu','nodo_padre','etiqueta','orden',)

