# Django
from django.urls import  path

# Views
from parametros.views.menus import CreateMenu,UpdateMenu
from parametros.views.nodosmenus import  NodoMenuDetailApi, NodoMenuUpdateApi, NodoMenuUpdateOrdenApi, NodoMenuUpdatePadreApi

urlpatterns =[
    path('api/parametros/menu/', CreateMenu.as_view(), name='menu_list'),
    path('api/parametros/menus/<int:pk>/', UpdateMenu.as_view(), name='menu_update'),

    path('api/parametros/nodo_menu/', NodoMenuDetailApi.as_view(), name='nodo_menu_list'),

    path('api/parametros/nodo_menu/<int:pk>/', NodoMenuUpdateApi.as_view(), name='nodo_menu_update'),

    path('api/parametros/nodo_menu/<int:pk>/orden/<int:orden>/', NodoMenuUpdateOrdenApi.as_view(), name='nodo_menu_orden'),
    path('api/parametros/nodo_menu/<int:pk>/padre/<int:padre_id>/', NodoMenuUpdatePadreApi.as_view(), name='nodo_menu_padre'),

    path('api/parametros/arbol_menu/<int:id_menu>/', NodoMenuUpdateApi.as_view(), name='nodo_arbol_menu'),

]
