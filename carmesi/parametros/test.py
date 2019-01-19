# third-party
from sequences import get_next_value
from parametros.utils import UtileriasParametroTest

# Django
from django.urls import resolve
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

# Models
from parametros.models import Menu, NodoMenu
from parametros.factories import ( MenuFactory, NodoMenuFactory, NodoMenuFactoryUtils )
from parametros.serializers import MenuSerializer, NodoMenuSerializer


class MenusModelTest(TestCase):
    def test_guardar_obtener_datos_menu(self):
        menu1 = Menu()
        menu1.nombre = 'Menu Patito'
        menu1.save()

        menu2 = Menu()
        menu2.nombre = 'Menu Gatito'
        menu2.save()

        menus_guardados = Menu.objects.all()
        self.assertEqual(menus_guardados.count(), 2)

        menu1_guardado = menus_guardados[0]
        menu2_guardado = menus_guardados[1]
        self.assertEqual(menu1_guardado.nombre, 'Menu Patito')
        self.assertEqual(menu2_guardado.nombre, 'Menu Gatito')

    def test_guardar_menu_nombre_vacio(self):
        menu_ = Menu()
        menu_.nombre = ''
        with self.assertRaises(ValidationError):
            menu_.save()
            menu_.full_clean() # SQLite no valida al guardar, es necesario este comando


    def test_guardar_menu_nombre_duplicado(self):
        menu_ = Menu()
        menu_.nombre = 'esto es una prueba'
        menu_.save()

        menu2_ = Menu()
        menu2_.nombre = 'esto es una prueba'

        with self.assertRaises(IntegrityError):
            menu2_.save()


class NodoMenuServiceTest(TestCase):

    def setUp(self):
        self.utilt = UtileriasParametroTest()
        self.menu = MenuFactory()
        get_next_value('nodosMenu', initial_value=0)


    def test_crear_nodomenu_principal(self):

        nodo = NodoMenuFactoryUtils.crear_nodo_menu(id= 1, nodo_padre=None, menu=self.menu)

        nodo_menus_guardados = NodoMenu.objects.all()
        self.assertEqual(nodo_menus_guardados[0].id_nodo_padre , None)
        self.assertEqual(nodo_menus_guardados.count(), 1)
        self.assertEqual(nodo_menus_guardados[0].nodo_padre , None)

    def test_crear_nodomenu_principal_con_id(self):
        nodo = NodoMenuFactoryUtils.crear_nodo_menu(id= 3, nodo_padre=None, menu=self.menu)
        nodo_menus_guardados = NodoMenu.objects.all()
        self.assertEqual(nodo_menus_guardados.count(), 1)
        self.assertEqual(nodo_menus_guardados[0].id , 3)


    def test_crear_nodomenu_con_padre(self):
        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id= None, nodo_padre=None, menu=self.menu)
        self.assertEquals(nodo_padre1.id,1)

        nodo2 = NodoMenuFactoryUtils.crear_nodo_menu(id= None, nodo_padre=nodo_padre1, menu=self.menu)

        self.assertEquals(nodo2.id, 2)
        self.assertEquals(nodo2.nodo_padre, nodo_padre1)

    def test_nonomenu_con_un_padre_y_un_menu_al_que_no_pertenece(self):
        menu2 = MenuFactory()

        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id= None, nodo_padre=None, menu=self.menu)

        nodo2 = NodoMenuFactoryUtils.crear_nodo_menu(id= None, nodo_padre=nodo_padre1, menu=menu2)

        self.assertEquals(nodo2.menu, self.menu)

    def test_crear_nodomenu_con_padre_que_no_existe(self):
        with self.assertRaises(ValidationError) as cm:
            nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=0, nodo_padre=10, menu=self.menu)
        error = cm.exception
        self.assertEquals(error.message,'El nodo padre con el id 10 no existe')

    def test_probar_el_generador_de_secuencias(self):
        siguiente = get_next_value('nodosMenu')
        self.assertEqual(siguiente, 1)
        siguiente = get_next_value('nodosMenu')
        self.assertEqual(siguiente, 2)
        siguiente = get_next_value()
        self.assertEqual(siguiente, 1)


    def test_crear_nodomenu_con_etiqueta_mayor_a_su_longitud_permitida(self):
        siguiente = get_next_value('nodosMenu')
        self.assertEquals(siguiente, 1)

        etiqueta ='a' * 100

        with self.assertRaises(ValidationError) as cm:
            nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu,etiqueta=etiqueta)

        error = cm.exception
        self.assertEquals(error.messages[0] ,'La longitud maxima es de '
                                            '60 caracteres (tiene 100)')
        siguiente = get_next_value('nodosMenu')
        self.assertEquals(siguiente, 2)

    def nodo_en_diccionario(self, nodo):
        dic_nodo = {'id': nodo.id,'menu':nodo.menu,'nodo_padre':nodo.nodo_padre, 'etiqueta': nodo.etiqueta, 'orden': nodo.orden}
        return dic_nodo

    def test_modificar_datos_nodo_menu(self):
        nodo_menu_data = NodoMenuFactoryUtils.crear_nodo_menu(id=3, nodo_padre=None, menu=self.menu)

        nodo_menu_data.etiqueta = 'Etiqueta modificada'
        nodo_menu_data.orden = 5
        nodo_update = self.nodo_en_diccionario(nodo_menu_data)
        nodo_modificado = NodoMenu.objects.modificarNodo(**nodo_update)
        self.assertEqual(nodo_modificado.etiqueta,'Etiqueta modificada')
        self.assertEqual(nodo_modificado.orden,1) #Aqui no se puede modificar el orden


    def test_modificar_nodo_con_menu_al_que_no_pertenece(self):
        menu2 = MenuFactory()

        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        nodo_padre2 = NodoMenuFactoryUtils.crear_nodo_menu(id=3, nodo_padre=nodo_padre1, menu=self.menu)

        nodo_padre2.menu = menu2

        nodo_update = self.nodo_en_diccionario(nodo_padre2)
        nodo_modificado = NodoMenu.objects.modificarNodo(**nodo_update)

        self.assertEquals(nodo_modificado.menu, self.menu)

    def test_al_crear_un_nodo_su_orden_es_el_mayor_de_su_nivel(self):
        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        NodoMenuFactoryUtils.crear_multiples_nodos_menu(4,self.menu, nodo_padre1)

        cantidad_nodos = NodoMenu.objects.get_cantidad_nodos_hijos(nodo_padre1.id)
        nodos_hijo = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)

        nodo_padre2 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        # Los nuevos nodos tiene el id desde el numero 2
        self.utilt.comparar_orden(nodo_padre1, [2, 3, 4, 5])

        self.assertEqual(nodo_padre1.orden,1)
        self.assertEqual(nodo_padre2.orden,2)


    def test_al_mover_orden_del_nodo(self):

        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        NodoMenuFactoryUtils.crear_multiples_nodos_menu(5, self.menu, nodo_padre1)
        cantidad_nodos = NodoMenu.objects.get_cantidad_nodos_hijos(nodo_padre1.id)

        nodos_hijo = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)

        # Los nuevos nodos tiene el id desde el numero 2
        self.utilt.comparar_orden(nodo_padre1, [2, 3, 4, 5, 6])

        NodoMenu.objects.cambiarOrden(6,1)
        self.utilt.comparar_orden(nodo_padre1, [6, 2, 3, 4, 5])


        NodoMenu.objects.cambiarOrden(4,2)
        self.utilt.comparar_orden(nodo_padre1, [6, 4, 2, 3, 5])


        NodoMenu.objects.cambiarOrden(6,5)

        cantidad_nodos = NodoMenu.objects.get_cantidad_nodos_hijos(nodo_padre1.id)
        self.utilt.comparar_orden(nodo_padre1, [4, 2, 3, 5,6])

        NodoMenu.objects.cambiarOrden(2,3)
        self.utilt.comparar_orden(nodo_padre1, [4, 3, 2, 5,6])



    def test_al_mover_orden_de_nodo_raiz(self):

        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        nodo_padre2 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        nodo_padre3 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)
        self.utilt.comparar_orden(None, [1, 2, 3])

        NodoMenu.objects.cambiarOrden(3,1)
        self.utilt.comparar_orden(None, [3, 1, 2])


    def test_al_mover_orden_que_no_existe(self):
        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        NodoMenuFactoryUtils.crear_multiples_nodos_menu(2,self.menu, nodo_padre1)
        cantidad_nodos = NodoMenu.objects.get_cantidad_nodos_hijos(nodo_padre1.id)

        with self.assertRaises(ValidationError) as cm:
             NodoMenu.objects.cambiarOrden(2,-1)

        error = cm.exception
        self.assertEquals(error.messages[0],'No se puede mover a un orden '
                                        'menor a 0')
        with self.assertRaises(ValidationError) as cm:
             NodoMenu.objects.cambiarOrden(2,3)
        error = cm.exception
        self.assertEquals(error.messages[0],'No se puede mover a un orden '
                                        'mayor al numero de elementos')

    def test_cambiar_nodo_de_padre_de_menu_diferente(self):
        menu2 = MenuFactory()

        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=menu2)

        nodo_padre2 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        self.assertEquals(nodo_padre1.id,1)
        self.assertEquals(nodo_padre2.id,2)

        with self.assertRaises(ValidationError) as cm:
             NodoMenu.objects.cambiar_nodo_padre(2,1)
        error = cm.exception
        self.assertEquals(error.message,'No se puede mover a un padre '
                                        'con menu diferente')


    def test_cambiar_nodo_de_padre(self):
        nodo_padre1= NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'Nodo Padre1',['p1h1','p1h2','p1h3'])
        nodo_padre2= NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'Nodo Padre2',['p2h1','p2h2','p2h3','p2h4'])


        nodos_hijo1 = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)
        nodos_hijo2 = NodoMenu.objects.get_nodos_hijos(nodo_padre2.id)
        self.assertEquals(nodos_hijo1.count(),3)
        self.assertEquals(nodos_hijo2.count(),4)

        self.utilt.comparar_orden(nodo_padre1, [2, 3, 4])
        self.utilt.comparar_orden(nodo_padre2, [6, 7, 8,9])

        NodoMenu.objects.cambiar_nodo_padre(7,1)

        nodos_hijo1 = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)
        nodos_hijo2 = NodoMenu.objects.get_nodos_hijos(nodo_padre2.id)
        self.assertEquals(nodos_hijo1.count(),4)
        self.assertEquals(nodos_hijo2.count(),3)

        self.utilt.comparar_orden(nodo_padre1, [2, 3, 4, 7])
        self.utilt.comparar_orden(nodo_padre2, [6, 8, 9])


    def test_eliminar_nodo(self):
        nodo_padre1 = NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, menu=self.menu)

        NodoMenuFactoryUtils.crear_multiples_nodos_menu(5,self.menu, nodo_padre1)

        nodos_hijo1 = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)
        self.utilt.comparar_orden(nodo_padre1, [2, 3, 4, 5, 6])

        eliminados = NodoMenu.objects.eliminar_nodo(4)
        self.assertEquals(eliminados,1)

        nodos_hijo1 = NodoMenu.objects.get_nodos_hijos(nodo_padre1.id)
        self.utilt.comparar_orden(nodo_padre1, [2, 3, 5, 6])

    def test_obtener_arbol_menu(self):
        NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'India',['AP','MP','KAR'])
        NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'UK',[])
        NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'Mexico',['Guadalajara','Sinaloa'])

        NodoMenuFactoryUtils.crear_nodo_con_hijos(self.menu,'KAR',['BAGDAG','MALGA'])

        NodoMenu.objects.cambiarOrden(6,1) #Ponemos a Mexico al Inicio del orden

        nodo_menu = NodoMenu.objects.obtener_arbol_menu(1)

        self.assertEqual(len(nodo_menu),3)
        self.assertEqual(nodo_menu[0]['etiqueta'],'Mexico')
        self.assertEqual(len(nodo_menu[0]['sub_menu']),2)

        self.assertEqual(nodo_menu[1]['etiqueta'],'India')
        self.assertEqual(len(nodo_menu[1]['sub_menu']),3)
        self.assertEqual(len(nodo_menu[1]['sub_menu'][2]['sub_menu']),2)

        self.assertEqual(nodo_menu[2]['etiqueta'],'UK')
        self.assertEqual(len(nodo_menu[2]['sub_menu']),0)

        nodo_menu_err = NodoMenu.objects.obtener_arbol_menu(3)

        self.assertEqual(len(nodo_menu_err),0)

