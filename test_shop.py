'''
Test per verificare la corrispondenza dei prezzi dei prodotti selezionati, le immagini e le quantità.
'''

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import random

#FUNZIONE AUSILIARIA CHE MI PERMETTE DI CONVERTIRE I PREZZI IN NUMERI COSI' POSSO FARE I CALCOLI
def price_converter(price):
    '''
    :param price: string
    :return: float price
    '''
    price = list(price)
    price.remove('€')
    price.remove(' ')
    for i, j in enumerate(price):
        price[i] = j.replace(',', '.')
    price = float(''.join(price))
    return price


class MyBagTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome() #QUI AGGIUNGO IL PATH AL CHROMEDRIVER
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
        products_name = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "box-title")))
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
        add_cart_btn = self.driver.find_element_by_xpath("//button[@id='add_cart_btn']")
        try:
            #not(self.driver.find_element_by_xpath("//p[@class='product-errormsg error-msg']").is_displayed())
            not(self.driver.find_element_by_xpath("//div[@class='alert alert-danger non-field-error']").is_displayed())
        except:
            print('Prodotto non disponibile')
            #ANDREBBE CONTROLLATO CHE IL CARRELLO RIMANE INALTERATO
        add_cart_btn.submit()#QUI SALTA TUTTA LA PARTE DELLA MODALE CON SUBMIT
        #ORA SONO NEL CARRELLO
        shopping_bag_prod = self.driver.find_element_by_xpath("//a[@class='cart-item']")
        shopping_bag_name = shopping_bag_prod.text
        #self.assertEqual(shopping_bag_name, check_name.text)
        shopping_bag_code = shopping_bag_prod.find_elements_by_xpath("span[@class='cart-details']")[1].text
        self.assertEqual(shopping_bag_code, product_code)
        shopping_bag_price = self.driver.find_elements_by_tag_name('td')[2].text #PREZZO è IL TERZO ELEMENTO DELLA RIGA
        shopping_bag_price = price_converter(shopping_bag_price)
        #shopping_bag_quantity = int(self.driver.find_elements_by_tag_name('td')[3].text)
        shopping_bag_total_price = self.driver.find_elements_by_tag_name('td')[4].text
        price_to_check = price_converter(shopping_bag_total_price)
        #CHECK SU PREZZO UNITARIO * QUANTITA' = PREZZO TOTALE
        self.assertEqual(price_to_check, shopping_bag_price) # DA AGGIUNGERE IL CHECK PER QUANTITA' * shopping_bag_quantity)
        #CHECKOUT
        checkout_area = self.driver.find_element_by_xpath("//div[@class='form-actions clearfix']")
        checkout_button = checkout_area.find_element_by_xpath("a[@class='btn btn-lg pull-right']")
        checkout_button.click()
        #INSERIRE I DATI PER L'ACQUISTO

    @classmethod
    def tearDownClass(cls):
       #close the browser window
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)


