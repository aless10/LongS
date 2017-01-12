'''
Test per verificare la corrispondenza dei prezzi dei prodotti selezionati, le immagini e le quantità.
'''

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import random


class MyBagTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome()#QUI AGGIUNGO IL PATH AL CHROMEDRIVER
        cls.driver.maximize_window()
        # navigate to the application home page
        cls.driver.get("http://dev:dev@ux.tannerie.doppiozero.to/it/")
        cls.current_page = "http://dev:dev@ux.tannerie.doppiozero.to/it/"

    def test_search_page(self):
        menu_elements = self.driver.find_elements_by_class_name('navigation-link')
        element = random.choice(menu_elements[:2])
        element.click()
        self.current_page = self.driver.current_url
        category = self.driver.find_elements_by_xpath("//a[@class='effect-bubba link-cat']")
        select_category = random.choice(category)
        select_category.click()
        products_name = self.driver.find_elements_by_xpath("//h2[@class='box-title']")
        products_price = self.driver.find_elements_by_xpath("//span[@class='price']")
        # DA AGGIUNGERE IL TRACCIAMENTO IMMAGINI PRODOTTO
        # scelgo un prodotto random
        rand_int = random.choice(range(len(products_name)))
        rand_product = (products_name[rand_int].text, products_price[rand_int].text)
        rand_prod_page = self.driver.find_element_by_partial_link_text(rand_product[0])
        self.assertTrue(rand_prod_page.is_displayed())
        rand_prod_page.click()
        self.current_page = self.driver.current_url
        #CHECK NOME ARTICOLO E PREZZO. QUI VA INSERITO UN CONTROLLO SU ARTICOLO DISPONIBILE O NO
        check_name = self.driver.find_element_by_xpath("//h1[@class='product-title']")
        check_price = self.driver.find_element_by_xpath("//p[@class='product-price']")
        #TEST SU NOME E PREZZO
        self.assertEqual(check_name.text, rand_product[0])
        self.assertEqual(check_price.text, rand_product[1])
        #SALVO IL CODICE PRODOTTO
        product_code = self.driver.find_element_by_xpath("//p[@class='product-code']").text
        #driver.save_screenshot('screenshot.png') #screenshot pagina
        add_cart_btn = self.driver.find_element_by_xpath("//button[@id='add_cart_btn']")
        print(add_cart_btn.location)
        # CLICCO SU ACQUISTA::: ERRORE NON MI VEDE/CLICCA IL BOTTONE
        add_cart_btn.click()
        #NAVIGO SULLA MODALE
        modal_page = self.driver.find_element_by_xpath("//div[@class='modal-body']")
        modal_prod_name = modal_page.find_element_by_xpath("//h4[@class='bold color-dorato']")
        modal_prod_name = modal_prod_name.text
        #CONTROLLO CHE IL NOME ARTICOLO SIA CORRETTO
        self.assertEqual(modal_prod_name, rand_product[0])
        modal_prod_code = modal_page.find_element_by_xpath("//p[@class='product-code']").text
        self.assertEqual(modal_prod_code, product_code)
        #AGGIUNGO AL CARRELLO
        modal_page.find_element_by_xpath("//a[@class='btn addedcart-btn pull-right']").click()


    @classmethod
    def tearDownClass(cls):
       #close the browser window
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)


