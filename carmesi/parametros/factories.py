# Models
from parametros.models import ( Menu, NodoMenu, )


# Factories
import factory
from faker import Factory

faker = Factory.create()

class MenuFactory(factory.DjangoModelFactory):
    class Meta:
        model = Menu
    nombre = factory.LazyAttribute(lambda _: faker.name())

class NodoMenuFactory(factory.DjangoModelFactory):
    class Meta:
        model = NodoMenu

    id = None
    menu = None
    nodo_padre = None
    etiqueta =   faker.name()
    orden = 0


    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return kwargs


class NodoMenuFactoryUtils():

    @staticmethod
    def crear_nodo_menu(id, nodo_padre, menu,etiqueta=None):
        nodo_data = NodoMenuFactory.build()

        nodo_data['id'] = id
        nodo_data['nodo_padre'] = nodo_padre
        nodo_data['menu'] = menu
        if etiqueta:
            nodo_data['etiqueta'] = etiqueta
        nodo = NodoMenu.objects.nuevoNodo(**nodo_data)
        return nodo

    @staticmethod
    def crear_multiples_nodos_menu(num_nodos, menu, nodo_padre):
        nodos_menu = NodoMenuFactory.build_batch(num_nodos, menu=menu, nodo_padre=nodo_padre)
        for nodo in nodos_menu:
            NodoMenu.objects.nuevoNodo(**nodo)
    @staticmethod
    def crear_nodo_con_hijos(menu, etiqueta_padre, hijos):
        filtro = {'etiqueta__exact': etiqueta_padre}
        nodo_padre = NodoMenu.objects.get_filtro(**filtro).first()


        if nodo_padre is None:
            nodo_padre= NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=None, etiqueta=etiqueta_padre ,menu=menu)

        for nodo in hijos:
            NodoMenuFactoryUtils.crear_nodo_menu(id=None, nodo_padre=nodo_padre, etiqueta=nodo ,menu=menu)
        return nodo_padre
