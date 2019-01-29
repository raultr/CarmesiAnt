# standar library
import json
import os
# third-party
from sequences import get_next_value

# Django
from django.urls import reverse
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, CoreAPIClient, RequestsClient

# Models
from parametros.models import Menu, NodoMenu
from parametros.serializers import MenuSerializer
from parametros.utils import UtileriasParametroTest

# Factories
from parametros.factories import ( MenuFactory, NodoMenuFactory, NodoMenuFactoryUtils )

class ParametroMenuAPITest(APITestCase):

    LOCAL_HOST = '' #"http://127.0.0.11:8000"
    staging_server = ""

    def setUp(self):

       self.base_url = reverse('menu_list')

       #self.client = RequestsClient()

       #self.staging_server = os.environ.get('STAGING_SERVER')
       #if not self.staging_server:
       #     self.staging_server = self.LOCAL_HOST

       self.base_url = f'{self.staging_server}{self.base_url}'

       #self.menu = MenuFactory.build()
       #self.nodoMenu = NodoMenuFactory()

    def post_menu_vacio(self):
        return self.client.post(
            self.base_url,
            {'nombre': ''}
        )

    def test_ruta(self):
        ruta =  '/api/parametros/menu/'

        ruta =f'{self.staging_server}{ruta}'
        self.assertEqual(self.base_url, ruta)

    def test_get_returns_json_200(self):
        self.client = APIClient()
        menu1 = Menu.objects.create(nombre="Menu Pato")
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_menus_guardados(self):
        menu1 = Menu.objects.create(nombre="Menu Pato")
        menu2 = Menu.objects.create(nombre="Menu Gato")
        response = self.client.get(self.base_url, format='json')
        self.assertEqual(json.loads(response.content.decode('utf8')),[{'id': 1, 'nombre': 'Menu Pato'}, {'id': 2, 'nombre': 'Menu Gato'}])

    def test_get_menu_id_guardado(self):
        menu1 = Menu.objects.create(nombre="Menu Pato")
        base_url_update = reverse('menu_update', kwargs={'pk': menu1.id})
        response = self.client.get(base_url_update, format='json')
        #response = self.client.get(f'{self.base_url}{menu1.id}/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf8')),{'id': 1, 'nombre': 'Menu Pato'} )

    def test_POSTing_nuevos_menu(self):
        menu_ = Menu.objects.create()
        response = self.client.post(self.base_url, {'menu': menu_.id, 'nombre': 'nuevo menu'})
        self.assertEqual(response.status_code, 201)
        menu_guardado = Menu.objects.get(nombre= 'nuevo menu')
        self.assertEqual(menu_guardado.nombre, "nuevo menu")

    def test_menu_vacio_no_se_puede_guardar(self):
        self.assertEqual(Menu.objects.count(),0)
        response = self.post_menu_vacio()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Menu.objects.count(),0)
        self.assertEqual(json.loads(response.content.decode('utf8')),{'nombre': ['This field may not be blank.']})

    def test_PUT_menu(self):
        menu1 = Menu.objects.create(nombre="Menu Pato")
        menu1 = Menu.objects.get(nombre='Menu Pato')
        self.assertEqual(menu1.nombre, 'Menu Pato')
        base_url_update = reverse('menu_update', kwargs={'pk': menu1.id})
        #self.assertEqual(f'{self.base_url}{menu1.id}/update/', base_url_update)
        #response = self.client.put(f'{self.base_url}{menu1.id}/update/', {'nombre': 'modificado menu'})
        response = self.client.put(base_url_update, {'nombre': 'modificado menu'})
        self.assertEqual(response.status_code, 200)
        menu1 = Menu.objects.all()
        self.assertEqual(menu1.count(), 1)
        self.assertEqual(menu1[0].nombre, 'modificado menu')

    def test_guardado_con_error(self):
        data = { 'nombre': ''}
        serializer = MenuSerializer(data=data)
        self.assertEqual(serializer.is_valid(),False)
        if serializer.is_valid():
            vote = serializer.save()

    def test_no_se_permiten_nombres_duplicados(self):
        self.client.post(self.base_url, {'nombre': "nuevo menu"})
        self.assertEqual( Menu.objects.all().count(), 1)
        response = self.client.post(self.base_url, {'nombre': 'nuevo menu'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Menu.objects.count(),1)
        self.assertEqual(json.loads(response.content.decode('utf8')),{'nombre': ['This field must be unique.']})

class ParametroNodoMenuAPITest(APITestCase):
    LOCAL_HOST = '' #"http://127.0.0.11:8000"
    staging_server = ""
    setup_done = False
    base_url = reverse('nodo_menu_list')
    client = CoreAPIClient()

    #base_url = '/api/parametros/nodo_menu/' #reverse('menu-list')

    def setUp(self):
       #import ipdb;ipdb.set_trace()
       if self.setup_done:
            return
       self.utilt = UtileriasParametroTest()
       #self.client = APIClient()
       self.menu = MenuFactory() #Menu.objects.create(nombre="Menu1")
       get_next_value('nodosMenu', initial_value=0)

       #self.staging_server = os.environ.get('STAGING_SERVER')
       #if not self.staging_server:
       #     self.staging_server = self.LOCAL_HOST

       self.base_url = f'{self.staging_server}{self.base_url}'


    def test_ruta(self):
        ruta = '/api/parametros/nodo_menu/'
        self.assertEqual(self.base_url,f'{self.staging_server}{ruta}')
        #response = self.client.get(self.base_url)
        #self.assertEqual(200, response.status_code)

    def test_POSTing_nuevos_nodomenu(self):
        data = {'id': '0',' menu': 1, 'nodo_padre': None, 'etiqueta':'Nodo Menu1','orden': 0}

        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, 201)
        menu_guardado = NodoMenu.objects.get(id= 1)
        self.assertEqual(menu_guardado.etiqueta, "Nodo Menu1")

    def test_POSTing_nuevos_nodomenu_con_id_consecutivo(self):
        data1 = {'id': '0',' menu': 1, 'nodo_padre': None, 'etiqueta':'Nodo Menu1','orden': 0}

        response1 = self.client.post(self.base_url, data1)

        self.assertEqual(response1.status_code, 201)
        menu_guardado = NodoMenu.objects.get(id= 1)
        self.assertEqual(menu_guardado.etiqueta, "Nodo Menu1")

        data2 = {'id': '0',' menu': 1, 'nodo_padre': None, 'etiqueta':'Nodo Menu1','orden': 0, 'etiqueta': 'Nodo Menu2'}

        response2 = self.client.post(self.base_url, data2)

        self.assertEqual(response2.status_code, 201)
        menu_guardado = NodoMenu.objects.get(id= 2)
        self.assertEqual(menu_guardado.etiqueta, "Nodo Menu2")



    def test_POSTing_nuevos_nodomenu_con_padre_que_no_exite(self):
        data = {'id': '0',' menu': 1, 'nodo_padre': 1, 'etiqueta':'Nodo Menu1','orden': 0}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,'El nodo padre con el id 1 no existe')


    def test_POSTing_nodomenu_con_etiqueta_mayor_a_su_longitud_permitida(self):
        etiqueta ='a' * 100
        data = {'id': '0',' menu': 1, 'nodo_padre': None, 'etiqueta':etiqueta,'orden': 0}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual( response.data['etiqueta'][0][0:] ,'La longitud '
                                    'maxima es de 60 caracteres (tiene 100)')

    def test_PUT_modificar_nodomenu(self):

        data = {'id': '0',' menu': 1, 'nodo_padre': None, 'etiqueta':'Etiqueta','orden': 0}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.data['id'],1)


        pk = response.data['id']

        base_url_update = reverse('nodo_menu_update', kwargs={'pk': pk})
        data_update = {'etiqueta': 'Etiqueta modificada'}

        response_update = self.client.put(base_url_update, data_update)

        self.assertEqual(response_update.status_code, 200)
        self.assertEqual( response_update.data['etiqueta'] ,'Etiqueta modificada')


    def test_PUT_modificar_etiqueta_mayor_a_su_longitud_permitida(self):

        data = {'id': '0',' menu': 1, 'nodo_padre': None, 'etiqueta':'Etiqueta','orden': 0}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.data['id'],1)

        pk = response.data['id']

        etiqueta ='a' * 100
        base_url_update = reverse('nodo_menu_update', kwargs={'pk': pk})
        data_update = {'etiqueta': etiqueta}

        response_update = self.client.put(base_url_update, data_update)

        self.assertEqual(response_update.status_code, 400)
        self.assertEqual( response_update.data['etiqueta'][0][0:] ,'La longitud maxima es de 60 caracteres (tiene 100)')

    def test_PUT_mover_orden_del_nodo(self):
        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        NodoMenuFactoryUtils.crear_multiples_nodos_menu(5, self.menu, nodo_padre1)

        cantidad_nodos = NodoMenu.objects.get_cantidad_nodos_hijos(nodo_padre1.id)

        nodos_hijo = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)

        self.utilt.comparar_orden(nodo_padre1, [2, 3, 4, 5, 6])
        base_url_orden = reverse('nodo_menu_orden', kwargs={'pk': 6, 'orden':1})
        response_update = self.client.put(base_url_orden)
        self.assertEqual(response_update.status_code, 200)


        self.utilt.comparar_orden(nodo_padre1, [6, 2, 3, 4, 5])

    def test_PUT_mover_orden_de_nodo_raiz(self):
        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        nodo_padre2 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        nodo_padre3 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        self.utilt.comparar_orden(None, [1, 2, 3])


        base_url_orden = reverse('nodo_menu_orden', kwargs={'pk': 3, 'orden':1})
        response_update = self.client.put(base_url_orden)
        self.assertEqual(response_update.status_code, 200)


        self.utilt.comparar_orden(None, [3, 1, 2])

    def test_PUT_mover_orden_que_no_existe(self):

        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        NodoMenuFactoryUtils.crear_multiples_nodos_menu(2,self.menu, nodo_padre1)
        cantidad_nodos = NodoMenu.objects.get_cantidad_nodos_hijos(nodo_padre1.id)


        base_url_orden = reverse('nodo_menu_orden', kwargs={'pk': 2, 'orden':3})

        response_update = self.client.put(base_url_orden)

        self.assertEqual(response_update.status_code, 400)
        self.assertEqual(response_update.data,'No se puede mover a un orden '
                                              'mayor al numero de elementos')

    def test_PUT_cambiar_nodo_de_padre_de_menu_diferente(self):
        menu2 = MenuFactory()

        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=menu2)

        nodo_padre2 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        self.assertEquals(nodo_padre1.id,1)
        self.assertEquals(nodo_padre2.id,2)

        base_url_orden = reverse('nodo_menu_padre', kwargs={'pk': 2, 'padre_id':1})

        response_update = self.client.put(base_url_orden)

        self.assertEqual(response_update.status_code, 400)
        self.assertEqual(response_update.data,'No se puede mover a un '
                                              'padre con menu diferente')

    def test_PUT_cambiar_nodo_de_padre(self):
        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        nodo_padre2 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        NodoMenuFactoryUtils.crear_multiples_nodos_menu(3,self.menu, nodo_padre1)
        NodoMenuFactoryUtils.crear_multiples_nodos_menu(4,self.menu, nodo_padre2)


        nodos_hijo1 = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)
        nodos_hijo2 = NodoMenu.objects.get_nodos_hijos(nodo_padre2.id)

        self.assertEquals(nodos_hijo1.count(),3)
        self.assertEquals(nodos_hijo2.count(),4)

        self.assertEqual(nodos_hijo2[1].id,7)


        base_url_orden = reverse('nodo_menu_padre', kwargs={'pk': 7, 'padre_id':1})

        response_update = self.client.put(base_url_orden)

        self.assertEqual(response_update.status_code, 200)
        self.assertEqual(response_update.data['id'],7)
        self.assertEqual(response_update.data['nodo_padre'],1)

    def test_DELETE_nodo(self):
        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        NodoMenuFactoryUtils.crear_multiples_nodos_menu(5,self.menu, nodo_padre1)

        nodos_hijo1 = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)

        self.utilt.comparar_orden(nodo_padre1, [2, 3, 4, 5, 6])


        base_url_update = reverse('nodo_menu_update', kwargs={'pk': 4})

        response_delete = self.client.delete(base_url_update)


        self.assertEqual(response_delete.status_code, 200)
        self.assertEquals(response_delete.data,1)

        nodos_hijo1 = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)
        self.utilt.comparar_orden(nodo_padre1, [2, 3, 5, 6])

    def test_GET_arbol_menu(self):
        NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'India',['AP','MP','KAR'])
        NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'UK',[])
        NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'Mexico',['Guadalajara','Sinaloa'])

        NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'KAR',['BAGDAG','MALGA'])

        NodoMenu.objects.cambiarOrden(6,1) #Ponemos a Mexico al Inicio del orden

        id_menu = 1
        base_url_arbol = reverse('nodo_arbol_menu', kwargs={'id_menu': id_menu})

        response = self.client.get(base_url_arbol, format='json')

        nodo_menu = json.loads(response.data)

        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(nodo_menu),3)
        self.assertEqual(nodo_menu[0]['etiqueta'],'Mexico')
        self.assertEqual(len(nodo_menu[0]['sub_menu']),2)

        self.assertEqual(nodo_menu[1]['etiqueta'],'India')
        self.assertEqual(len(nodo_menu[1]['sub_menu']),3)
        self.assertEqual(len(nodo_menu[1]['sub_menu'][2]['sub_menu']),2)

        self.assertEqual(nodo_menu[2]['etiqueta'],'UK')
        self.assertEqual(len(nodo_menu[2]['sub_menu']),0)

        id_menu = 3
        base_url_arbol = reverse('nodo_arbol_menu', kwargs={'id_menu': id_menu})

        response = self.client.get(base_url_arbol, format='json')
        self.assertEquals(response.data,'[]')

    def test_probandoError(self):
        self.assertEqual(2,3)

