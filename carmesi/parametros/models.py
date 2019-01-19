# standar library
import json
import copy
# third.party
from sequences import get_next_value

# Django
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import transaction
from django.db.models import F

# Exceptions


ERROR_CAMPO_VACIO = 'El campo no puede estar vacio'
ERROR_VALOR_NULO = 'No se admiten valores nulos'
ERROR_ID_NO_EXISTE = "El {} con el id {} no existe"
ERROR_LONGITUD = "La longitud maxima es de %(limit_value)d caracteres (tiene %(show_value)d)"
ERROR_VALOR_MINIMO = "No se puede mover a un orden menor a 0"


validar_nombre = RegexValidator(regex=r'^[A-Za-záéíóúáéíóúÁÉÍÓÚ]+$',
                                message= ("El nombre no puede estar vacios"))

def buscarId(model, id, descripcion):
    try:
        return model.objects.get(id=id)
    except model.DoesNotExist:
         raise ValidationError(ERROR_ID_NO_EXISTE.format(descripcion, id))

class Menu(models.Model):
    nombre = models.TextField(blank=False, default= '', unique=True,  error_messages={'blank':ERROR_CAMPO_VACIO, 'null': ERROR_VALOR_NULO,  'unique': "Ya existe ese menu"},validators=[validar_nombre])

#    def __str__:
#        return self.nombre

class NodoMenuQuerySet(models.query.QuerySet):

    def get_filtro(self, **filtros):
        return self.filter(**filtros)

    def get_arbol_menu(self, id_menu, columna_orden):
        return self.filter(menu = id_menu)
        #.order_by(columna_orden)

    def get_nodos_hijo(self,nodo_padre):
        return self.filter(nodo_padre=nodo_padre)

    def get_cantidad_nodos_hijos(self, nodo_padre):
        return self.filter(nodo_padre=nodo_padre).count()

class NodoMenuManager(models.Manager):
    def get_queryset(self):
        return NodoMenuQuerySet(self.model, using=self._db)

    def get_filtro(self, **filtros):
         return self.get_queryset().get_filtro(**filtros)

    def get_arbol_menu(self, id_menu, columna_orden):
        return self.get_queryset().get_arbol_menu(id_menu, columna_orden)

    def get_nodos_hijos(self, nodo_padre):
        return self.get_queryset().get_nodos_hijo(nodo_padre)

    def get_cantidad_nodos_hijos(self, nodo_padre):
        return self.get_queryset().get_cantidad_nodos_hijos(nodo_padre)

    def asignar_nodo_padre(self, nodo_padre):
        if(str(nodo_padre).isdigit()):
            nodo_padre = buscarId(NodoMenu, nodo_padre, 'nodo padre')
        return None if nodo_padre == 'None' else nodo_padre

    def asginar_menu(self,nodo_padre, menu):
        if(nodo_padre != None):
            menu = nodo_padre.menu
        return menu

    def asigar_menu_y_nodo_padre(self,nodo_padre, menu):
        nodo_padre = self.asignar_nodo_padre(nodo_padre)
        menu = self.asginar_menu(nodo_padre, menu)
        return {'nodo_padre':nodo_padre, 'menu':menu}

    def asignar_orden(self, nodo_padre):
        cantidad_nodos = self.get_cantidad_nodos_hijos(nodo_padre)
        return cantidad_nodos + 1


    @transaction.atomic
    def cambiar_nodo_padre(self,id_hijo,nodo_padre_nuevo):
        nodo_padre = self.asignar_nodo_padre(nodo_padre_nuevo)
        orden = self.asignar_orden(nodo_padre_nuevo)

        nodo_hijo = self.asignar_nodo_padre(id_hijo)

        self.validarCambioDeNodoPadre(nodo_padre, nodo_hijo)

        nodo_ant = copy.deepcopy(nodo_hijo)

        nodo_hijo.nodo_padre=nodo_padre
        nodo_hijo.orden = orden

        nodo_hijo.full_clean()
        nodo_hijo.save()

        self.filter(nodo_padre=nodo_ant.id_nodo_padre, orden__gte=nodo_ant.orden).update(orden=F('orden') - 1)
        return nodo_hijo


    @transaction.atomic
    def nuevoNodo(self,id,menu,nodo_padre,etiqueta,orden):
        padre = self.asigar_menu_y_nodo_padre(nodo_padre, menu)
        orden = self.asignar_orden(padre['nodo_padre'])

        nodo_menu = self.model(
            id= get_next_value('nodosMenu') if id == None or id=='0' or id==0 else id,
            menu=padre['menu'],
            nodo_padre=padre['nodo_padre'],
            etiqueta=etiqueta,
            orden=orden)
        nodo_menu.full_clean()
        nodo_menu.save()

        return nodo_menu

    @transaction.atomic
    def modificarNodo(self,id, etiqueta,**kwargs):
        nodo_menu = buscarId(NodoMenu, id, 'id')
        nodo_menu.etiqueta = etiqueta
        nodo_menu.full_clean()
        nodo_menu.save()
        return nodo_menu

    @transaction.atomic
    def eliminar_nodo(self,id):
        nodo_menu = buscarId(NodoMenu, id, 'id')

        desde = nodo_menu.orden
        sum_res = 1

        eliminados = nodo_menu.delete()

        self.filter(nodo_padre=nodo_menu.id_nodo_padre, orden__gte=desde).update(orden=F('orden') - sum_res)


        return eliminados[0]

    def validarCambioOrden(self, id_padre, nuevo_orden):
        num_hijos = self.get_cantidad_nodos_hijos(id_padre)
        if(nuevo_orden> num_hijos):
            raise ValidationError('No se puede mover a un orden mayor '
                                  'al numero de elementos')

    def validarCambioDeNodoPadre(self,nodo_padre, id_hijo):
        if(nodo_padre.menu !=  id_hijo.menu):
            raise ValidationError('No se puede mover a un padre '
                                  'con menu diferente')

    def definirRangoOrdenModificar(self, orden_act, nuevo_orden):
        desde = orden_act + 1
        hasta = nuevo_orden
        sum_res =  -1

        if(orden_act> nuevo_orden):
            desde = nuevo_orden
            hasta = orden_act -1
            sum_res = 1
        return [desde, hasta, sum_res]

    @transaction.atomic
    def cambiarOrden(self, id, nuevo_orden):
        nodo_menu = buscarId(NodoMenu, id, 'id')

        self.validarCambioOrden(nodo_menu.id_nodo_padre, nuevo_orden)

        desde,hasta,sum_res = self.definirRangoOrdenModificar(nodo_menu.orden, nuevo_orden)

        self.filter(nodo_padre=nodo_menu.id_nodo_padre, orden__gte=desde, orden__lte = hasta).update(orden=F('orden') + sum_res)
        nodo_menu.orden = nuevo_orden
        nodo_menu.full_clean()
        nodo_menu.save()
        return nodo_menu

    def obtener_arbol_menu(self, id_menu, format_json= False):
        nodos_menu = self.get_arbol_menu(id_menu, 'orden')
        nodo_menu_ordenado =sorted(nodos_menu, key=lambda x: x.orden)

        arbol_menu = self.construir_arbol_menu(nodo_menu_ordenado, None)

        return arbol_menu if format_json == False else  json.dumps(arbol_menu)

    def construir_arbol_menu(self, nodos_menu, id_padre):
        arbol_menu = [{'id': nodo.id, 'etiqueta': nodo.etiqueta,
                       'nodo_padre': nodo.id_nodo_padre,
                       'orden': nodo.orden,
                       'sub_menu': self.construir_arbol_menu(nodos_menu, nodo.id) }
                    for nodo in nodos_menu if  nodo.id_nodo_padre == id_padre]
        return arbol_menu


class NodoMenu(models.Model):
    id = models.IntegerField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    nodo_padre = models.ForeignKey('self', null=True, blank=True, related_name='subnodomenu', on_delete=models.PROTECT)
    etiqueta = models.CharField(max_length=60,
        error_messages={'max_length': ERROR_LONGITUD})
    orden = models.PositiveIntegerField(validators=[MinValueValidator(0)],
        error_messages={'min_value': ERROR_VALOR_MINIMO})

    @property
    def id_nodo_padre(self):
        return None if self.nodo_padre == None else self.nodo_padre.id


    #objects = NodoMenuQuerySet.as_manager()
    objects = NodoMenuManager()
