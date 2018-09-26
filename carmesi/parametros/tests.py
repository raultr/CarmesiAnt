from django.urls import resolve
from django.test import TestCase
from django.test import TestCase
from parametros.models import Menu

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


# class HomePageTest(TestCase):

#     def test_root_url_resolves_to_home_page_view(self):
#             found = resolve('/')
#             self.assertEqual(found.func, home_page)

