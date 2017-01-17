'''
Test per verificare la corrispondenza dei prezzi dei prodotti selezionati, le immagini e le quantità.
Completamento acquisto prodotto
'''

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions
import random
from doppiozero_test.test_tannery_doppiozero.config import base_url
from time import gmtime, strftime, sleep
from doppiozero_test.test_tannery_doppiozero.utils import price_converter


class BuyAProductTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome() #QUI AGGIUNGO IL PATH AL CHROMEDRIVER
        cls.driver.maximize_window()
        # navigate to the application home page
        cls.driver.get(base_url)

    def test_search_page(self):
        self.driver.find_element_by_xpath("//a[@id='cookieChoiceDismiss']").click()
        menu_elements = self.driver.find_elements_by_class_name('navigation-link')
        element = random.choice(menu_elements[:1])
        element.click()
        #PAGINA DELLE CATEGORIE PRODOTTO
        category = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.\
                                                       XPATH, "//a[@class='effect-bubba link-cat']")))
        select_category = random.choice(category)
        select_category.click()
        #PAGINA PRODOTTI
        products_name = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "box-title")))
        products_price = self.driver.find_elements_by_xpath("//span[@class='price']")
        # DA AGGIUNGERE IL TRACCIAMENTO IMMAGINI PRODOTTO
        # scelgo un prodotto random
        rand_int = random.choice(range(len(products_name)))
        rand_product = (products_name[rand_int].text, products_price[rand_int].text)
        rand_prod_page = self.driver.find_element_by_partial_link_text(rand_product[0])
        self.assertTrue(rand_prod_page.is_displayed())
        rand_prod_page.click()
        #CHECK NOME ARTICOLO E PREZZO. QUI VA INSERITO UN CONTROLLO SU ARTICOLO DISPONIBILE O NO

        check_name = self.driver.find_element_by_xpath("//h1[@class='product-title']").text
        check_price = self.driver.find_element_by_xpath("//p[@class='product-price']").text
        #TEST SU NOME E PREZZO
        self.assertEqual(check_name, rand_product[0])
        self.assertEqual(check_price, rand_product[1])
        #SALVO IL CODICE PRODOTTO
        product_code = self.driver.find_element_by_xpath("//p[@class='product-code']").text
        WebDriverWait(self.driver, 10).until(\
            expected_conditions.invisibility_of_element_located((By.XPATH, "//input[@type='hidden']")))
        WebDriverWait(self.driver, 10).until(\
            expected_conditions.invisibility_of_element_located((By.XPATH, "//input[@type='hidden']")))
        WebDriverWait(self.driver, 10).until( \
            expected_conditions.invisibility_of_element_located((By.XPATH, "//input[@id='id_quantity']")))
        WebDriverWait(self.driver, 10).until( \
            expected_conditions.invisibility_of_element_located((By.XPATH, "//select[@id='id_option2']")))
        add_cart_btn = self.driver.find_element_by_xpath("//button[@id='add_cart_btn']")
        add_cart_btn.submit()
        # #QUI SALTA TUTTA LA PARTE DELLA MODALE CON SUBMIT
        #add_cart_btn.click()
        # WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class='modal-body']")))
        # modal_page_name = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'bold color-dorato'))).text
        # self.assertEqual(modal_page_name, check_name)
        # modal_page_code = self.driver.find_element_by_xpath("//p[@class='product-code']")
        # self.assertEqual(modal_page_code.text, product_code)
        # modal_page_button = self.driver.find_element_by_xpath("//button[@class='btn addedcart-btn pull-left']")
        # modal_page_button.click()
        #ORA SONO NEL CARRELLO
        shopping_bag_prod = self.driver.find_element_by_xpath("//a[@class='cart-item']")
        shopping_bag_name = shopping_bag_prod.find_element_by_xpath("//strong").text
        #TEST NOME PRODOTTO
        self.assertEqual(shopping_bag_name, check_name)
        shopping_bag_code = shopping_bag_prod.find_elements_by_xpath("span[@class='cart-details']")[1].text
        #TEST CODICE PRODOTTO
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
        checkout_button = checkout_area.find_element_by_xpath("//a[@class='btn btn-lg pull-right']")
        checkout_button.click()
        #CHECK DATI MOSTRATI
        resume_div = self.driver.find_element_by_xpath("//div[@class='media-body text-left']")
        self.assertIn(check_name, resume_div.text)
        self.assertIn(check_price, resume_div.text)
        #INSERIRE I DATI PER L'ACQUISTO
        first_name = self.driver.find_element_by_id("id_billing_detail_first_name")
        first_name.send_keys('Test Name')
        last_name = self.driver.find_element_by_id("id_billing_detail_last_name")
        last_name.send_keys(strftime("%Y%m%d%H%M%S", gmtime()))
        address = self.driver.find_element_by_id("id_billing_detail_street")
        address.send_keys('Test Street')
        city = self.driver.find_element_by_id("id_billing_detail_city")
        city.send_keys('Test city')
        state = Select(self.driver.find_element_by_id("id_billing_detail_state"))
        selected_state = state.select_by_visible_text("Austria")
        postal_code = self.driver.find_element_by_id("id_billing_detail_postcode")
        postal_code.send_keys('9999')
        phone = self.driver.find_element_by_id("id_billing_detail_phone")
        phone.send_keys('112')
        email_address = self.driver.find_element_by_id("id_billing_detail_email")
        email_address.send_keys('test@example.com')
        text_area = self.driver.find_element_by_id("id_additional_instructions")
        text_area.send_keys('Test Additional Instruction')
        terms_and_conditions = WebDriverWait(self.driver, 20).until(\
            expected_conditions.presence_of_all_elements_located((By.ID, "condizioni")))[0]
        self.assertFalse(terms_and_conditions.is_selected())
        terms_and_conditions.submit()
        submit_button = self.driver.find_element_by_xpath("//button[@id='checkout_next' and @value='Prossimo']")
        submit_button.click()
        #PAGINA PAGAMENTO PAYPAL
        sleep(2)
        iframe = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(iframe)
        email_address = self.driver.find_element_by_xpath("//input[@placeholder='Indirizzo email']")
        email_address.send_keys('andrea.doppiozero-buyer@gmail.com')
        password = self.driver.find_element_by_id('password')
        password.send_keys('Nonlaso00')
        self.driver.find_element_by_id('btnLogin').submit()
        #DA AGGIUNGERE I CHECK PREZZI
        check_out_paypal = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.ID, "confirmButtonTop")))
        check_out_paypal.click()
        sleep(5)
        self.assertEqual(self.driver.current_url, "http://ux.tannerie.doppiozero.to/it/shop/checkout/complete/")

    @classmethod
    def tearDownClass(cls):
    #    #close the browser window
         cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)


