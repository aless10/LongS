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
from .config import *
from time import gmtime, strftime, sleep
from .utils import *


class BuyAProductTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome('/home/ale/VirtuaPyCharm/bin/chrome/chromedriver') #QUI AGGIUNGO IL PATH AL CHROMEDRIVER
        cls.driver.maximize_window()
        cls.tannerie = Tannerie()
        # navigate to the application home page
        cls.driver.get(base_url)

    def test_buy_and_checkout(self):
        self.driver.find_element_by_xpath(self.tannerie.get_cookie()).click()
        #PAGINA PRODOTTI
        n = 0
        products_info = {}
        while n < num_elements_to_test:
            products_name = WebDriverWait(self.driver, 20).until(\
                                    expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "box-title")))
            products_price = self.driver.find_elements_by_xpath("//span[@class='price']")
            # scelgo un prodotto random
            rand_int = random.choice(range(len(products_name)-1))
            rand_product = (products_name[rand_int].text, price_converter(products_price[rand_int].text))
            rand_prod_page = self.driver.find_element_by_partial_link_text(rand_product[0])
            self.assertTrue(rand_prod_page.is_displayed())
            rand_prod_page.click()
            check_name = self.driver.find_element_by_xpath("//h1[@class='product-title']").text
            check_price = price_converter(self.driver.find_element_by_xpath("//p[@class='product-price']").text)
            #TEST SU NOME E PREZZO
            self.assertEqual(check_name, rand_product[0])
            self.assertEqual(check_price, rand_product[1])
            #SALVO IL CODICE PRODOTTO
            product_code = slice_code(self.driver.find_element_by_xpath("//p[@class='product-code']").text)
            #ATTENDO CHE I CAMPI HIDDEN SIANO NASCOSTI
            WebDriverWait(self.driver, 10).until(\
                expected_conditions.invisibility_of_element_located((By.XPATH, "//input[@type='hidden']")))
            WebDriverWait(self.driver, 10).until(\
                expected_conditions.invisibility_of_element_located((By.XPATH, "//input[@type='hidden']")))
            WebDriverWait(self.driver, 10).until( \
                expected_conditions.invisibility_of_element_located((By.XPATH, "//input[@id='id_quantity']")))
            WebDriverWait(self.driver, 10).until( \
                expected_conditions.invisibility_of_element_located((By.XPATH, "//select[@id='id_option2']")))
            add_cart_btn = self.driver.find_element_by_xpath("//button[@id='add_cart_btn']")
            add_cart_btn.click()

            modal_page = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((\
                                            By.CLASS_NAME, 'modal' and 'fade' and 'addedcart' and 'in')))
            modal_page_name = self.driver.find_element_by_xpath("//h4[@class='bold color-dorato']").text
            self.assertEqual(modal_page_name, check_name)
            modal_page_code = slice_code(self.driver.find_element_by_xpath("//p[@class='product-code']").text)
            self.assertEqual(modal_page_code, product_code)
            products_info['product ' + str(n)] = {'name': rand_product[0], 'price': rand_product[1], 'code': product_code}
            if n != num_elements_to_test - 1:
                modal_page_button = self.driver.find_element(By.CLASS_NAME, 'btn' and 'addedcart-btn' and 'pull-left')
                modal_page_button.click()
                sleep(2)
                WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'productBack'))).click()
                sleep(2)
            else:
                modal_page_button = self.driver.find_element(By.CLASS_NAME, 'btn' and 'addedcart-btn' and 'pull-right')
                modal_page_button.click()
            n += 1

        #ORA SONO NEL CARRELLO
        total_price = check_products_prizes(self.driver, products_info)
        # cart_table = self.driver.find_element_by_xpath("//tbody")
        # cart_rows = cart_table.find_elements_by_tag_name('tr')
        # cart_rows.pop()
        # total_price = 0
        # n = 0
        # for row in cart_rows:
        #     shopping_bag_prod = row.find_elements_by_tag_name('td')[1]
        #     shopping_bag_name = shopping_bag_prod.find_element_by_xpath("//strong").text
        #     print(shopping_bag_name, n)
        #     #self.assertEqual(shopping_bag_name, products_info['product ' + str(n)]['name'])
        #     shopping_bag_code = slice_code(shopping_bag_prod.find_elements_by_xpath("//span[@class='cart-details']")[1].text)
        #     print(shopping_bag_prod, n)
        #     #TEST CODICE PRODOTTO
        #     #self.assertEqual(shopping_bag_code, products_info['product ' + str(n)]['code'])
        #     shopping_bag_price_1 = row.find_elements_by_tag_name('td')[2].text
        #     shopping_bag_price = price_converter(shopping_bag_price_1)
        #     print(shopping_bag_price)
        #     self.assertEqual(shopping_bag_price, products_info['product ' + str(n)]['price'])
        #     quantity = row.find_elements_by_tag_name('td')[3]
        #     shopping_bag_quantity = int(quantity.find_element_by_tag_name('input').get_attribute('value'))
        #     shopping_bag_total_price = row.find_elements_by_tag_name('td')[4].text
        #     price_to_check = price_converter(shopping_bag_total_price)
        #     # CHECK SU PREZZO UNITARIO * QUANTITA' = PREZZO TOTALE
        #     self.assertEqual(price_to_check, shopping_bag_price * shopping_bag_quantity)
        #     total_price += price_to_check
        #     n += 1

        total_shopping_bag = slice_prod_price(self.driver.find_element_by_xpath("//div[@class='total']").text)
        total_shopping_bag = price_converter(total_shopping_bag)
        self.assertEqual(total_price, total_shopping_bag)

        #CHECKOUT
        checkout_area = self.driver.find_element_by_xpath("//div[@class='form-actions clearfix']")
        checkout_button = checkout_area.find_element_by_xpath("//a[@class='btn btn-lg pull-right']")
        checkout_button.click()
        #CHECK DATI MOSTRATI
        # product_list = self.driver.find_elements_by_xpath("//li[@class='media']")
        # check_out_total = 0
        # for product in product_list:
        #     #resume_div_name = slice_prod_name(product.text)
        #     resume_div_price = price_converter(slice_prod_price(product.text))
        #     check_out_total += resume_div_price
        check_out_total = check_out_total_func(self.driver)
        total = self.driver.find_element_by_xpath("//div[@class='total']").text
        total = price_converter(slice_prod_price(total))
        self.assertEqual(total, check_out_total)

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
        random_state = random.choice(list(states))
        selected_state = state.select_by_visible_text(random_state)
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
        #FINE INSERIMENTO DATI

        #TEST SUI PREZZI SINGOLI E TOTALI
        check_out_total = check_out_total_func(self.driver)
        # product_list = self.driver.find_elements_by_xpath("//li[@class='media']")
        # check_out_total = 0
        # for product in product_list:
        #     # resume_div_name = slice_prod_name(product.text)
        #     resume_div_price = price_converter(slice_prod_price(product.text))
        #     check_out_total += resume_div_price
        sub_total = price_converter(slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[0].text))
        shipping = price_converter(slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[1].text))
        self.assertEqual(check_out_total, sub_total)
        self.assertEqual(states[random_state], shipping)
        total = self.driver.find_element_by_xpath("//div[@class='total']").text
        total = price_converter(slice_prod_price(total))
        self.assertEqual(total, sub_total + shipping)

        #TORNO AL CARRELLO
        cart = self.driver.find_element_by_xpath("//a[@class='btn']")
        cart.click()
        sub_total_cart = price_converter(\
            slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[0].text))
        shipping_cart = price_converter(\
            slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[1].text))
        self.assertEqual(check_out_total, sub_total_cart)
        self.assertEqual(states[random_state], shipping_cart)
        total_cart = self.driver.find_element_by_xpath("//div[@class='total']").text
        total_cart = price_converter(slice_prod_price(total_cart))
        self.assertEqual(total_cart, sub_total_cart + shipping_cart)

        #FACCIO L'UPDATE DELLE QUANTITA'
        change_quantity = self.driver.find_elements_by_xpath("//input[@id='id_items-0-quantity']")
        random_update = random.choice(change_quantity)
        self.driver.execute_script("arguments[0].value = '2';", random_update)
        update = self.driver.find_elements_by_xpath("//button[@class='cart-update']")[0]
        update.click()
        sleep(2)
        # CHECK DEI VALORI
        new_total_price = check_products_prizes(self.driver, products_info)
        sub_total_cart = price_converter( \
            slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[0].text))
        shipping_cart = price_converter( \
            slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[1].text))
        self.assertEqual(new_total_price, sub_total_cart)
        self.assertEqual(states[random_state], shipping_cart)
        total_cart = self.driver.find_element_by_xpath("//div[@class='total']").text
        total_cart = price_converter(slice_prod_price(total_cart))
        self.assertEqual(total_cart, sub_total_cart + shipping_cart)
        checkout_area = self.driver.find_element_by_xpath("//div[@class='form-actions clearfix']")
        checkout_button = checkout_area.find_element_by_xpath("//a[@class='btn btn-lg pull-right']")
        checkout_button.click()

        # product_list = self.driver.find_elements_by_xpath("//li[@class='media']")
        # check_out_total = 0
        # for product in product_list:
        #     # resume_div_name = slice_prod_name(product.text)
        #     resume_div_price = price_converter(slice_prod_price(product.text))
        #     check_out_total += resume_div_price
        check_out_total = check_out_total_func(self.driver)
        sub_total = price_converter(
            slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[0].text))
        shipping = price_converter(
            slice_prod_price(self.driver.find_elements_by_xpath("//div[@class='order-totals']//div")[1].text))
        self.assertEqual(check_out_total, sub_total)
        self.assertEqual(sub_total_cart, sub_total)
        self.assertEqual(states[random_state], shipping)
        total = self.driver.find_element_by_xpath("//div[@class='total']").text
        total = price_converter(slice_prod_price(total))
        self.assertEqual(total, sub_total + shipping)

        submit_button = self.driver.find_element_by_xpath("//button[@id='checkout_next' and @value='Prossimo']")
        submit_button.click()
        #PAGINA PAGAMENTO PAYPAL
        sleep(2)
        #CHECK PAGAMENTO
        paypal_price = self.driver.find_element_by_xpath("//span[@class='ltrOverride ng-binding']").text.split(' E')[0]
        paypal_price = price_converter('€ ' + paypal_price)
        self.assertEqual(paypal_price, total)
        iframe = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(iframe)
        email_address = self.driver.find_element_by_xpath("//input[@placeholder='Indirizzo email']")
        email_address.send_keys(email)
        password_driver = self.driver.find_element_by_id('password')
        password_driver.send_keys(password)
        self.driver.find_element_by_id('btnLogin').submit()
        check_out_paypal = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.ID, "confirmButtonTop")))
        # CHECK PAGAMENTO
        paypal_price = price_converter(
            '€ ' + self.driver.find_element_by_xpath("//span[@class='ltrOverride ng-binding']").text.split(' E')[0])
        self.assertEqual(paypal_price, total)
        # check_out_paypal.click()
        # sleep(5)
        # self.assertEqual(self.driver.current_url, "http://ux.tannerie.doppiozero.to/it/shop/checkout/complete/")

    # @classmethod
    # def tearDownClass(cls):
    # # #    #close the browser window
    #     cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)


