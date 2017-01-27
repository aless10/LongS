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
from selenium.common.exceptions import NoSuchElementException
import random
from config import *
from utils import *


class BuyAProductTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome(path_to_chrome) #QUI AGGIUNGO IL PATH AL CHROMEDRIVER
        cls.driver.maximize_window()
        cls.company = site
        # navigate to the application home page
        cls.driver.get(cls.company.get_url())

    def test_buy_and_checkout(self):
        self.driver.find_element_by_xpath(self.company.get_cookie()).click()
        sleep(2)
        #PAGINA PRODOTTI
        n = 0
        products_info = {}
        while n < num_elements_to_test:
            products_name = WebDriverWait(self.driver, 20).until(\
                            expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, self.company.get_products_name())))
            products_price = self.driver.find_elements_by_xpath(self.company.get_price())

            # scelgo un prodotto random
            rand_int = random.choice(range(len(products_name)-1))
            rand_product = (products_name[rand_int].text, price_converter(products_price[rand_int].get_attribute('innerHTML')))
            rand_prod_page = self.driver.find_elements_by_xpath(self.company.get_product_page_link())[rand_int]
            self.assertTrue(rand_prod_page.is_displayed())
            rand_prod_page.click()

            #------PAGINA PRODOTTO-------

            check_name = self.driver.find_element_by_xpath(self.company.get_single_product_name()).text
            check_price = price_converter(self.driver.find_element_by_xpath(self.company.get_single_product_price()).text)
            #TEST SU NOME E PREZZO
            self.assertEqual(check_name, rand_product[0])
            self.assertEqual(check_price, rand_product[1])
            #SALVO IL CODICE PRODOTTO
            if self.company.get_code():
                right_div = self.driver.find_element_by_xpath(\
                    "//div[@class='product-info__description']/label[@class='product-info__label']")
                product_code = right_div.find_elements_by_xpath("//div[@class='product-info__description']")[1].text
                product_code = slice_code(product_code)
            else:
                product_code = slice_code(self.driver.find_element_by_xpath(self.company.get_product_code()).text)

            if self.company.wait_for_hidden():
                WebDriverWait(self.driver, 10).until(\
                    expected_conditions.invisibility_of_element_located((By.XPATH, "//input[@type='hidden']")))
                WebDriverWait(self.driver, 10).until(\
                    expected_conditions.invisibility_of_element_located((By.XPATH, "//input[@type='hidden']")))
                WebDriverWait(self.driver, 10).until( \
                    expected_conditions.invisibility_of_element_located((By.XPATH, "//input[@id='id_quantity']")))
                WebDriverWait(self.driver, 10).until( \
                    expected_conditions.invisibility_of_element_located((By.XPATH, "//select[@id='id_option2']")))

            add_cart_btn = self.driver.find_element_by_xpath(self.company.add_cart_btn())
            sleep(2)
            add_cart_btn.click()
            if self.company.is_modal():
                modal_page = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((\
                                            By.CLASS_NAME, 'modal' and 'fade' and 'addedcart' and 'in')))
                modal_page = self.driver.find_element_by_xpath(self.company.get_modal_page_name())
                modal_page_name = modal_page.text
                #modal_page_name = modal_page.find_element_by_xpath(self.company.get_modal_page_name()).text
                self.assertEqual(modal_page_name, check_name)
                if self.company.modal_page_code():
                    modal_page_code = slice_code(self.driver.find_element_by_xpath("//p[@class='product-code']").text)
                    self.assertEqual(modal_page_code, product_code)

                products_info['product ' + str(n)] = {'name': rand_product[0], 'price': rand_product[1], 'code': product_code}
                if n != num_elements_to_test - 1:
                    modal_page_button = self.driver.find_element(By.CLASS_NAME, self.company.continue_button())
                    modal_page_button.click()
                    sleep(2)
                    # QUESTI SI CHIAMANO IN DUE MODI DIVERSI
                    # PER ORA LO METTO PERSONALIZZATO
                    if self.company.back_to_shop():
                        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'productBack'))).click()
                    else:
                        WebDriverWait(self.driver, 10).until(\
                        expected_conditions.element_to_be_clickable((By.XPATH, "//a[@href='/shop/']"))).click()
                    sleep(2)
                else:
                    modal_page_button = self.driver.find_element(By.CLASS_NAME, self.company.shopping_bag_button())
                    modal_page_button.click()
                n += 1

        #ORA SONO NEL CARRELLO

        total_price = check_products_prizes(self, self.driver, products_info)
        total_shopping_bag = slice_prod_price(self.driver.find_element_by_xpath(self.company.get_total_price()).text)
        total_shopping_bag = price_converter(total_shopping_bag)
        self.assertEqual(total_price, total_shopping_bag)

        #CHECKOUT
        checkout_button = self.driver.find_element_by_xpath(self.company.go_check_out())
        checkout_button.click()

        check_out_total = check_out_total_func(self.driver)
        total = self.driver.find_element_by_xpath(self.company.get_total_price()).text
        total = price_converter(slice_prod_price(total))
        #self.assertEqual(total, check_out_total)

        #INSERIRE I DATI PER L'ACQUISTO
        sleep(2)
        first_name = self.driver.find_element_by_id(self.company.get_user_data()['first_name'])
        first_name.send_keys('Test Name')
        last_name = self.driver.find_element_by_id(self.company.get_user_data()['last_name'])
        last_name.send_keys(strftime("%Y%m%d%H%M%S", gmtime()))
        address = self.driver.find_element_by_id(self.company.get_user_data()['street'])
        address.send_keys('Test Street')
        city = self.driver.find_element_by_id(self.company.get_user_data()['city'])
        city.send_keys('Test city')
        state = Select(self.driver.find_element_by_id(self.company.get_user_data()['state']))
        random_state = random.choice(list(self.company.states()))
        selected_state = state.select_by_visible_text(random_state)
        postal_code = self.driver.find_element_by_id(self.company.get_user_data()['postcode'])
        postal_code.send_keys('9999')
        phone = self.driver.find_element_by_id(self.company.get_user_data()['phone'])
        phone.send_keys('112')
        email_address = self.driver.find_element_by_id(self.company.get_user_data()['email'])
        email_address.send_keys('test@example.com')
        text_area = self.driver.find_element_by_id(self.company.get_user_data()['add_instruction'])
        text_area.send_keys('Test Additional Instruction')
        terms_and_conditions = WebDriverWait(self.driver, 20).until(\
            expected_conditions.presence_of_all_elements_located((By.ID, self.company.terms_and_conditions())))[0]
        self.assertFalse(terms_and_conditions.is_selected())
        terms_and_conditions.submit()
        #FINE INSERIMENTO DATI

        #TEST SUI PREZZI SINGOLI E TOTALI
        check_out_total = check_out_total_func(self.driver)
        total = self.driver.find_element_by_xpath(self.company.get_total_price()).text
        total = price_converter(slice_prod_price(total))
        if self.company.pay_ship():
            sub_total = price_converter(\
                slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[0].text))
            shipping = price_converter(\
                slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[1].text))
            self.assertEqual(states[random_state], shipping)
            self.assertEqual(check_out_total, sub_total)
            self.assertEqual(total, sub_total + shipping)
        else:
            self.assertEqual(total, check_out_total)

        #TORNO AL CARRELLO
        cart = self.driver.find_element_by_xpath(self.company.button_back_paypal())
        cart.click()
        sub_total_cart = price_converter(\
            slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[0].text))
        if self.company.pay_ship():
            shipping_cart = price_converter(\
                slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[1].text))
            self.assertEqual(states[random_state], shipping_cart)
        else:
            shipping_cart = 0
        self.assertEqual(check_out_total, sub_total_cart)
        total_cart = self.driver.find_element_by_xpath(self.company.get_total_price()).text
        total_cart = price_converter(slice_prod_price(total_cart))
        self.assertEqual(total_cart, sub_total_cart + shipping_cart)

        #FACCIO L'UPDATE DELLE QUANTITA'
        change_quantity = self.driver.find_elements_by_xpath(self.company.update_quantity())
        random_update = random.choice(change_quantity)
        self.driver.execute_script("arguments[0].value = '2';", random_update)
        update = self.driver.find_elements_by_xpath(self.company.update_cart_btn())[0]
        update.click()
        sleep(2)
        # CHECK DEI VALORI
        new_total_price = check_products_prizes(self, self.driver, products_info)
        if self.company.pay_ship():
            sub_total_cart = price_converter( \
                slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[0].text))
            shipping_cart = price_converter( \
                slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[1].text))
            self.assertEqual(new_total_price, sub_total_cart)
            self.assertEqual(states[random_state], shipping_cart)
        else:
            shipping_cart = 0
        total_cart = self.driver.find_element_by_xpath(self.company.get_total_price()).text
        total_cart = price_converter(slice_prod_price(total_cart))
        self.assertEqual(total_cart, sub_total_cart + shipping_cart)
        #checkout_area = self.driver.find_element_by_xpath("//div[@class='form-actions clearfix']")
        checkout_button = self.driver.find_element_by_xpath(self.company.go_check_out())
        checkout_button.click()

        check_out_total = check_out_total_func(self.driver)
        sub_total = price_converter(
            slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[0].text))
        shipping = price_converter(
            slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[1].text))
        self.assertEqual(check_out_total, sub_total)
        self.assertEqual(sub_total_cart, sub_total)
        self.assertEqual(states[random_state], shipping)
        total = self.driver.find_element_by_xpath(self.company.get_total_price()).text
        total = price_converter(slice_prod_price(total))
        self.assertEqual(total, sub_total + shipping)

        terms_and_conditions = WebDriverWait(self.driver, 20).until( \
            expected_conditions.presence_of_all_elements_located((By.ID, self.company.terms_and_conditions())))[0]
        #self.assertFalse(terms_and_conditions.is_selected())
        terms_and_conditions.submit()

        submit_button = self.driver.find_element_by_xpath(self.company.checkout_paypal())
        submit_button.click()
        #PAGINA PAGAMENTO PAYPAL
        sleep(2)
        if self.company.road_to_paypal():
            money = float(self.driver.find_element_by_xpath("//span[@class='value']"))
            self.assertEqual(money, total)
            self.driver.find_element_by_xpath("//input[@value='08000001_Pay']").submit()
            self.driver.find_element_by_xpath("//input[@id='confirm']").submit

        #CHECK PAGAMENTO PAYPAL
        paypal_price = self.driver.find_element_by_xpath(self.company.pay_pal_price()).text.split(' E')[0]
        paypal_price = price_converter('€ ' + paypal_price)
        self.assertEqual(paypal_price, total)
        iframe = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(iframe)
        email_address = self.driver.find_element_by_xpath("//input[@placeholder='Indirizzo email']")
        email_address.send_keys(email)
        password_driver = self.driver.find_element_by_id('password')
        password_driver.send_keys(password)
        self.driver.find_element_by_id('btnLogin').submit()
        check_out_paypal = WebDriverWait(self.driver, 20).until(\
            expected_conditions.presence_of_element_located((By.ID, "confirmButtonTop")))

        # CHECK PAGAMENTO
        paypal_price = price_converter(
            '€ ' + self.driver.find_element_by_xpath(self.company.pay_pal_price()).text.split(' E')[0])
        self.assertEqual(paypal_price, total)
        # check_out_paypal.click()
        # sleep(5)
        # self.assertEqual(self.driver.current_url, "http://ux.tannerie.doppiozero.to/it/shop/checkout/complete/")

    # @classmethod
    # def tearDownClass(cls):
    # #    #close the browser window
    #     cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
