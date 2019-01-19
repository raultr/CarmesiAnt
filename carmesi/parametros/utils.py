# Django
from django.test import TestCase

# Models
from parametros.models import Menu, NodoMenu

class UtileriasParametroTest(TestCase):

    def comparar_orden(self, nodo_padre, ids_en_orden):
        cantidad_nodos = NodoMenu.objects.get_cantidad_nodos_hijos(nodo_padre)

        nodos_hijo = NodoMenu.objects.get_nodos_hijos(nodo_padre)

        self.assertEqual(cantidad_nodos, len(ids_en_orden))

        i = 0
        while i < cantidad_nodos:
            id_nodo = nodos_hijo[i].id
            id_orden =  nodos_hijo[i].orden
            orden = ids_en_orden.index(nodos_hijo[i].id) + 1
            self.assertEqual(nodos_hijo[i].orden, orden)
            i += 1
