
# standar library

# Django
from rest_framework import generics

# Models Serializers
from parametros.models.menus import Menu
from parametros.serializers.menus import MenuSerializer


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
