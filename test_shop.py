import unittest
from selenium import webdriver
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
import random
import config


class CheckoutTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome(config.path_to_chrome)
        cls.driver.maximize_window()
        # navigate to the application home page
        cls.driver.get(config.base_url)

    @classmethod
    def tearDownClass(cls):
        # close the browser window
        cls.driver.quit()

    def test_home(self):
        login = self.driver.find_element_by_xpath("/html/body/div[1]/esselunga-welcome-header/header/div/p/a[1]")
        login.click()
        mail_field = self.driver.find_element_by_id("gw_username")
        mail_field.send_keys(config.email)
        password_field = self.driver.find_element_by_id("gw_password")
        password_field.send_keys(config.password)
        remember_me = self.driver.find_element_by_id("rememberme")
        remember_me.click()
        login = self.driver.find_element_by_xpath("//*[@id='loginForm']/div/button")
        login.click()
        self.assertEqual(self.driver.title, 'Esselunga a casa - Home')
        # Go checkout!
        go_checkout = self.driver.find_element_by_id("cassa")
        go_checkout.click()

        slots = self.driver.find_elements_by_xpath("//input[@class='disponibile']")

        if slots:
            print(f"{len(slots)} slots found.")
            slots[0].click()
            self.driver.save_screenshot(f"{datetime.datetime.now()}_slots_found.png")
            self.driver.find_elements_by_xpath("//*[@id='checkoutNextStep']")[0].click()
            self.driver.save_screenshot(f"{datetime.datetime.now()}_payment_method.png")
            self.driver.find_elements_by_xpath("//*[@id='checkoutNextStep']")[0].click()
        else:
            print("No slot available")
        assert True

    # def test_buy_and_checkout(self):
    #     try:
    #         os.mkdir('./' + site_choice)
    #     except:
    #         pass
    #     self.driver.find_element_by_xpath(self.company.get_cookie()).click()
    #     sleep(2)
    #     #PAGINA PRODOTTI
    #     n = 0
    #     products_info = {}
    #     while n < num_elements_to_test:
    #         products_name = WebDriverWait(self.driver, 20).until(
    #                         expected_conditions.presence_of_all_elements_located((By.XPATH, self.company.get_products_name())))
    #         products_price = self.driver.find_elements_by_xpath(self.company.get_price())
    #
    #         # scelgo un prodotto random
    #         rand_int = random.choice(range(len(products_name)-1))
    #         rand_product = (products_name[rand_int].text, price_converter(products_price[rand_int].get_attribute('innerHTML')))
    #         rand_prod_page = self.driver.find_elements_by_xpath(self.company.get_product_page_link())[rand_int]
    #         self.assertTrue(rand_prod_page.is_displayed())
    #         rand_prod_page.click()
    #
    #         #------PAGINA PRODOTTO-------
    #
    #         try:
    #             check_name = self.driver.find_element_by_xpath(self.company.get_single_product_name()).text
    #             check_price = price_converter(self.driver.find_element_by_xpath(self.company.get_single_product_price()).text)
    #             #TEST SU NOME E PREZZO
    #             self.assertEqual(check_name, rand_product[0])
    #             self.assertEqual(check_price, rand_product[1])
    #         except:
    #             screen_name = 'product_price_name_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #             self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #             raise
    #
    #         #SALVO IL CODICE PRODOTTO
    #         if self.company.get_code():
    #             right_div = self.driver.find_element_by_xpath(
    #                 self.company.get_product_code()[0])
    #             product_code = right_div.find_elements_by_xpath(self.company.get_product_code()[1])[1].text
    #             product_code = slice_code(product_code)
    #         else:
    #             product_code = slice_code(self.driver.find_element_by_xpath(self.company.get_product_code()).text)
    #
    #         if self.company.wait_for_hidden_fields():
    #             WebDriverWait(self.driver, 10).until(
    #                 expected_conditions.invisibility_of_element_located((By.XPATH, self.company.wait_for_hidden()[0])))
    #             WebDriverWait(self.driver, 10).until(
    #                 expected_conditions.invisibility_of_element_located((By.XPATH, self.company.wait_for_hidden()[1])))
    #             WebDriverWait(self.driver, 10).until(
    #                 expected_conditions.invisibility_of_element_located((By.XPATH, self.company.wait_for_hidden()[2])))
    #             WebDriverWait(self.driver, 10).until(
    #                 expected_conditions.invisibility_of_element_located((By.XPATH, self.company.wait_for_hidden()[3])))
    #
    #         add_cart_btn = self.driver.find_element_by_xpath(self.company.add_cart_btn())
    #         sleep(2)
    #         add_cart_btn.click()
    #         if self.company.is_modal():
    #             modal_page = WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((
    #                                         By.ID, self.company.modal_id())))
    #             modal_page = self.driver.find_element_by_xpath(self.company.get_modal_page_name())
    #             modal_page_name = modal_page.text
    #             self.assertEqual(modal_page_name, check_name)
    #             if self.company.modal_page_code():
    #                 try:
    #                     modal_page_code = slice_code(self.driver.find_element_by_xpath(self.company.get_product_code()).text)
    #                     self.assertEqual(modal_page_code, product_code)
    #                 except:
    #                     screen_name = 'modal_code_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #                     self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #
    #             products_info['product ' + str(n)] = {'name': rand_product[0], 'price': rand_product[1], 'code': product_code}
    #             if n != num_elements_to_test - 1:
    #                 modal_page_button = self.driver.find_element(By.CLASS_NAME, self.company.continue_button())
    #                 modal_page_button.click()
    #                 sleep(2)
    #                 # QUESTI SI CHIAMANO IN DUE MODI DIVERSI
    #                 # PER ORA LO METTO PERSONALIZZATO
    #                 if self.company.back_to_shop():
    #                     WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'productBack'))).click()
    #                 else:
    #                     WebDriverWait(self.driver, 10).until(
    #                     expected_conditions.element_to_be_clickable((By.XPATH, "//a[@href='/shop/']"))).click()
    #                 sleep(2)
    #             else:
    #                 modal_page_button = self.driver.find_element(By.CLASS_NAME, self.company.shopping_bag_button())
    #                 modal_page_button.click()
    #             n += 1
    #
    #     #ORA SONO NEL CARRELLO
    #
    #     total_price = check_products_prizes(self, self.driver, products_info)
    #     try:
    #         total_shopping_bag = slice_prod_price(self.driver.find_element_by_xpath(self.company.get_total_price()).text)
    #         total_shopping_bag = price_converter(total_shopping_bag)
    #         self.assertEqual(total_price, total_shopping_bag)
    #     except:
    #         screen_name = 'total_shopping_bag_price_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #         self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #
    #     #CHECKOUT
    #     checkout_button = self.driver.find_element_by_xpath(self.company.go_check_out())
    #     checkout_button.click()
    #     sleep(1)
    #     try:
    #         check_out_total = check_out_total_func(self.driver)
    #         total = self.driver.find_element_by_xpath(self.company.get_total_price()).text
    #         total = price_converter(slice_prod_price(total))
    #         self.assertEqual(total, check_out_total)
    #     except:
    #         screen_name = 'product_total_price_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #         self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #
    #     #INSERIRE I DATI PER L'ACQUISTO
    #     sleep(2)
    #     first_name = self.driver.find_element_by_id(self.company.get_user_data()['first_name'])
    #     first_name.send_keys('Test Name')
    #     last_name = self.driver.find_element_by_id(self.company.get_user_data()['last_name'])
    #     last_name.send_keys(strftime("%Y/%m/%d - %H:%M:%S", gmtime()))
    #     address = self.driver.find_element_by_id(self.company.get_user_data()['street'])
    #     address.send_keys('Test Street')
    #     city = self.driver.find_element_by_id(self.company.get_user_data()['city'])
    #     city.send_keys('Test city')
    #     if self.company.select_state():
    #         state = Select(self.driver.find_element_by_id(self.company.get_user_data()['state']))
    #         random_state = random.choice(list(self.company.states()))
    #         selected_state = state.select_by_visible_text(random_state)
    #     else:
    #         random_state = random.choice(list(self.company.states()))
    #         box_state = self.driver.find_element_by_id(self.company.path_to_select_state()[0])
    #         box_state.click()
    #         input_box = self.driver.find_element_by_xpath(self.company.path_to_select_state()[1]).send_keys(random_state)
    #         self.driver.find_element_by_xpath(self.company.path_to_select_state()[2]).click()
    #     postal_code = self.driver.find_element_by_id(self.company.get_user_data()['postcode'])
    #     postal_code.send_keys('9999')
    #     phone = self.driver.find_element_by_id(self.company.get_user_data()['phone'])
    #     phone.send_keys('112')
    #     email_address = self.driver.find_element_by_id(self.company.get_user_data()['email'])
    #     email_address.send_keys('test@example.com')
    #     text_area = self.driver.find_element_by_id(self.company.get_user_data()['add_instruction'])
    #     text_area.send_keys('Test Additional Instruction')
    #     terms_and_conditions = WebDriverWait(self.driver, 20).until(
    #           expected_conditions.presence_of_element_located((By.XPATH, self.company.terms_and_conditions()))).click()
    #     self.driver.find_element_by_xpath(self.company.checkout_paypal()).click()
    #     #FINE INSERIMENTO DATI
    #
    #     #TEST SUI PREZZI SINGOLI E TOTALI
    #     check_out_total = check_out_total_func(self.driver)
    #     total = self.driver.find_element_by_xpath(self.company.get_total_price()).text
    #     total = price_converter(slice_prod_price(total))
    #     if self.company.pay_ship():
    #         try:
    #             sub_total = price_converter(
    #                 slice_prod_price(self.driver.find_elements_by_xpath(self.company.get_sub_total_price())[0].text))
    #             shipping = price_converter(
    #                 slice_prod_price(self.driver.find_elements_by_xpath(self.company.get_sub_total_price())[1].text))
    #             self.assertEqual(self.company.states()[random_state], shipping)
    #             self.assertEqual(check_out_total, sub_total)
    #             self.assertEqual(total, sub_total + shipping)
    #         except NoSuchElementException:
    #             screen_name = 'checkout_total_price_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #             self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #     else:
    #         try:
    #             self.assertEqual(total, check_out_total)
    #         except:
    #             screen_name = 'checkout_total_price_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #             self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #
    #     #TORNO AL CARRELLO
    #     cart = self.driver.find_element_by_xpath(self.company.button_back_paypal())
    #     cart.click()
    #     sub_total_cart = price_converter(
    #         slice_prod_price(self.driver.find_elements_by_xpath(self.company.get_sub_total_price())[0].text))
    #     if self.company.pay_ship():
    #         shipping_cart = price_converter(
    #             slice_prod_price(self.driver.find_elements_by_xpath(self.company.get_sub_total_price())[1].text))
    #         self.assertEqual(self.company.states()[random_state], shipping_cart)
    #     else:
    #         shipping_cart = 0
    #
    #     try:
    #         self.assertEqual(check_out_total, sub_total_cart)
    #         total_cart = self.driver.find_element_by_xpath(self.company.get_total_price()).text
    #         total_cart = price_converter(slice_prod_price(total_cart))
    #         self.assertEqual(total_cart, sub_total_cart + shipping_cart)
    #     except:
    #         screen_name = 'cart_total_price_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #         self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #
    #     #FACCIO L'UPDATE DELLE QUANTITA'
    #     change_quantity = self.driver.find_elements_by_xpath(self.company.update_quantity())
    #     random_update = random.choice(change_quantity)
    #     self.driver.execute_script("arguments[0].value = '2';", random_update)
    #     update = self.driver.find_elements_by_xpath(self.company.update_cart_btn())[0]
    #     update.click()
    #     sleep(2)
    #     # CHECK DEI VALORI
    #     new_total_price = check_products_prizes(self, self.driver, products_info)
    #     if self.company.pay_ship():
    #         sub_total_cart = price_converter(
    #             slice_prod_price(self.driver.find_elements_by_xpath(self.company.get_sub_total_price())[0].text))
    #         shipping_cart = price_converter(
    #             slice_prod_price(self.driver.find_elements_by_xpath(self.company.get_sub_total_price())[1].text))
    #         self.assertEqual(new_total_price, sub_total_cart)
    #         self.assertEqual(self.company.states()[random_state], shipping_cart)
    #     else:
    #         shipping_cart = 0
    #         sub_total_cart = new_total_price
    #     total_cart = self.driver.find_element_by_xpath(self.company.get_total_price()).text
    #     total_cart = price_converter(slice_prod_price(total_cart))
    #     try:
    #         self.assertEqual(total_cart, sub_total_cart + shipping_cart)
    #     except:
    #         screen_name = 'update_cart_total_price_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #         self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #
    #     checkout_button = self.driver.find_element_by_xpath(self.company.go_check_out())
    #     checkout_button.click()
    #
    #     check_out_total = check_out_total_func(self.driver)
    #     sub_total = price_converter(
    #         slice_prod_price(self.driver.find_elements_by_xpath(self.company.get_sub_total_price())[0].text))
    #     if self.company.pay_ship():
    #         shipping = price_converter(
    #             slice_prod_price(self.driver.find_elements_by_xpath(self.company.get_sub_total_price())[1].text))
    #         self.assertEqual(self.company.states()[random_state], shipping)
    #     else:
    #         shipping = 0
    #
    #     #self.assertEqual(check_out_total, sub_total)
    #     try:
    #         total = self.driver.find_element_by_xpath(self.company.get_total_price()).text
    #         total = price_converter(slice_prod_price(total))
    #         self.assertEqual(sub_total_cart, sub_total)
    #         self.assertEqual(total, sub_total + shipping)
    #     except:
    #         screen_name = 'update_checkout_total_price_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #         self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #
    #     if self.company.return_to_terms_and_conditions():
    #         terms_and_conditions = WebDriverWait(self.driver, 20).until(
    #             expected_conditions.presence_of_element_located((By.XPATH, self.company.terms_and_conditions())))
    #         self.assertFalse(terms_and_conditions.is_selected())
    #         terms_and_conditions.submit()
    #     sleep(2)
    #     submit_button = self.driver.find_element_by_xpath(self.company.checkout_paypal())
    #     submit_button.click()
    #     sleep(2)
    #
    #     #SE PRIMA BISOGNA ANDARE SU BNL O ALTRO (QUESTO PER PLM)
    #     if self.company.road_to_paypal():
    #         money = float(price_converter(self.driver.find_elements_by_xpath(self.company.bnl_frame()[0])[-1].text))
    #         self.assertEqual(money, total)
    #         options = self.driver.find_elements_by_xpath(self.company.bnl_frame()[1])[-1]
    #         options.click()
    #         sleep(2)
    #         self.driver.execute_script(self.company.bnl_frame()[2])
    #         sleep(2)
    #
    #     #PAGINA PAGAMENTO PAYPAL
    #     #CHECK PAGAMENTO PAYPAL
    #     try:
    #         paypal_price = self.driver.find_elements_by_xpath(self.company.pay_pal_price())[0].text.split(' E')[0]
    #         paypal_price = price_converter('€ ' + paypal_price)
    #         self.assertEqual(paypal_price, total)
    #     except:
    #         screen_name = 'paypal_total_price_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #         self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #
    #     iframe = self.driver.find_elements_by_tag_name(self.company.i_frame()[0])[0]
    #     self.driver.switch_to.frame(iframe)
    #     email_address = self.driver.find_element_by_xpath(self.company.i_frame()[1])
    #     email_address.send_keys(email)
    #     password_driver = self.driver.find_element_by_id(self.company.i_frame()[2])
    #     password_driver.send_keys(password)
    #     self.driver.find_element_by_id(self.company.i_frame()[3]).submit()
    #     check_out_paypal = WebDriverWait(self.driver, 20).until(\
    #         expected_conditions.presence_of_element_located((By.ID, self.company.i_frame()[4])))
    #
    #     # CHECK PAGAMENTO
    #     try:
    #         paypal_price = price_converter(
    #              '€ ' + self.driver.find_element_by_xpath(self.company.pay_pal_price()).text.split(' E')[0])
    #         self.assertEqual(paypal_price, total)
    #     except:
    #         screen_name = 'final_paypal_total_price_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #         self.driver.save_screenshot(os.path.join(site_choice, screen_name))
    #     # check_out_paypal.click()
    #     # sleep(5)
    #     #try:
    #         # self.assertEqual(self.driver.current_url, self.company.complete_url())
    #     #except:
    #         #screen_name = 'url_page_error_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.png'
    #         #self.driver.save_screenshot(os.path.join(site_choice, screen_name))



if __name__ == '__main__':
    unittest.main(verbosity=2)
