# standar library
import os

# third.party
from selenium import webdriver
import unittest

#  Django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
#from django.test import LiveServerTestCase
#from django.test import Client

class NuevoVisitanteTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        #self.client = Client()

    def tearDown(self):
        self.browser.quit()

    def test_puede_ver_la_pagina(self):
        #self.assertEquals(self.live_server_url,'')
        ruta = self.live_server_url + '/api/parametros/menu/'
        self.browser.get(ruta)
        #self.browser.get('http://localhost:8000/api/parametros/menu/')
        #response = self.client.get('/api/parametros/menu/')
        #self.assertTemplateUsed(response, 'home.html')
        self.assertIn('Django REST framework', self.browser.title)
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
