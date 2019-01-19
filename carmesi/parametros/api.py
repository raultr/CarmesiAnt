
# standar library
import json
from functools import wraps

# Django
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets

# Models Serializers
from parametros.models import Menu, NodoMenu
from parametros.serializers import MenuSerializer, NodoMenuSerializer,NodoMenuUpdateSerializer


# POST (201 CREATED) 400
# GET (200 OK) (404 NOT FOUND) (400 BAD REQUEST)
# PUT (200 OK) (404 NOT FOUND)
# DELETE (200 OK) (404 NOT FOUND)

class CreateMenu(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

class UpdateMenu(generics.RetrieveUpdateAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()


def procesar(func):
   @wraps(func)
   def wrapper(request, serializer, serializer_out=None,validated_serializer=False,**kwds):
       try:
           if(validated_serializer):
                serializ = serializer(data= request.data)
                serializ.is_valid(raise_exception=True)
                serializ.validated_data.update(**kwds)
                nodo = func(**serializ.validated_data)
           else:
                nodo = func(**kwds)
       except ValidationError as e:
           return Response(e.message,status=status.HTTP_400_BAD_REQUEST)
       serializer = serializer if serializer_out == None else serializer_out
       respuesta = nodo if serializer== None else serializer(nodo).data
       return Response(respuesta, status=get_statusHTTP(request.method))
   return wrapper

def get_statusHTTP(method):
    if(method in('POST')):
        return status.HTTP_201_CREATED
    if(method in('GET','PUT','DELETE')):
        return status.HTTP_200_OK


class NodoMenuDetailApi(APIView):

    def post(self, request):
        #serializer = NodoMenuSerializer(data= request.data)
        #serializer.is_valid(raise_exception=True)
        #serializer.validated_data['id_nodo_padre'] = request.data['id_nodo_padre']
        parametros = {'nodo_padre': request.data['nodo_padre']}
        respuesta = procesar(NodoMenu.objects.nuevoNodo)
        return respuesta(request,serializer= NodoMenuSerializer, validated_serializer=True, **parametros)

class NodoMenuUpdateApi(APIView):
    def get(self, request, id_menu):
        parametros = {'id_menu': id_menu, 'format_json': True }
        respuesta = procesar(NodoMenu.objects.obtener_arbol_menu)

        return respuesta(request, serializer= None,  **parametros)

    def put(self, request, pk):
        #serializer = NodoMenuUpdateSerializer(pk, data= request.data)
        #serializer.is_valid(raise_exception=True)
        #serializer.validated_data['id']=pk
        parametros = {'id': pk}

        respuesta = procesar(NodoMenu.objects.modificarNodo)
        return respuesta(request, serializer= NodoMenuUpdateSerializer,serializer_out=NodoMenuSerializer, validated_serializer=True , **parametros)

    def delete(self, request, pk):
        parametros = {'id': pk }
        respuesta = procesar(NodoMenu.objects.eliminar_nodo)
        return respuesta(request, serializer= None,
                         **parametros)


class NodoMenuUpdateOrdenApi(APIView):

    def put(self, request, pk, orden):
        parametros = {'id': pk, 'nuevo_orden': orden}
        respuesta = procesar(NodoMenu.objects.cambiarOrden)
        return respuesta(request, serializer= NodoMenuSerializer,  **parametros)


class NodoMenuUpdatePadreApi(APIView):

    def put(self, request, pk, padre_id):
        parametros = {'id_hijo': pk, 'nodo_padre_nuevo': padre_id}
        respuesta = procesar(NodoMenu.objects.cambiar_nodo_padre)
        return respuesta(request, serializer= NodoMenuSerializer,  **parametros)
