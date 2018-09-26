from selenium import webdriver
import unittest




class AppCarmesiTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_start(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('RedGranatum 2018',  self.browser.title)
        self.fail('Test Terminado')

if __name__ == '__main__':
    unittest.main(warnings= 'ignore')
