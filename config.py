'''
Dati di configurazione e avvio per il test su tannery
'''

from time import gmtime, strftime, sleep

# percorso per caricare il chromedriver
path_to_chrome = '/home/ale/VirtuaPyCharm/bin/chrome/chromedriver'
num_elements_to_test = 2
email = 'andrea.doppiozero-buyer@gmail.com'
password = 'Nonlaso00'
states = {'Austria': 15.0, 'Italia': 10.0, 'USA': 35.0}
site_to_test = ['tannerie', 'plm', ]


class Company(object):

    def wait_for_hidden(self):
        return True

    def get_code(self):
        return False

    def is_modal(self):
        return True

    def modal_page_code(self):
        return True

    def back_to_shop(self):
        return True

    def pay_ship(self):
        return True

    def road_to_paypal(self):
        return True

    def get_cookie(self):
        return "//a[@id='cookieChoiceDismiss']"

    def get_price(self):
        return "//span[@class='price']"

    def add_cart_btn(self):
        return "//button[@id='add_cart_btn']"

    def get_total_price(self):
        return "//div[@class='total']"

    def get_user_data(self):
        user_data = {
        'first_name' : "id_billing_detail_first_name",
        'last_name' : "id_billing_detail_last_name",
        'street' : "id_billing_detail_street",
        'city' : "id_billing_detail_city",
        'state' : "id_billing_detail_state",
        'postcode' : "id_billing_detail_postcode",
        'phone' : "id_billing_detail_phone",
        'email' : "id_billing_detail_email",
        'add_instruction' : "id_additional_instructions",
        }
        return user_data

    def button_back_paypal(self):
        return "//button[@name='back']"

    def update_quantity(self):
        return "//input[@id='id_items-0-quantity']"

    def pay_pal_price(self):
        return "//span[@class='ltrOverride ng-binding']"


class Tannerie(Company):

    def road_to_paypal(self):
        return False

    def get_url(self):
        base_url = 'http://dev:dev@ux.tannerie.doppiozero.to/it/donna/?cat%5B%5D=Borse+a+mano'
        return base_url

    def get_products_name(self):
        return "box-title"

    def get_product_code(self):
        return "//p[@class='product-code']"

    def get_single_product_name(self):
        return "//h1[@class='product-title']"

    def get_single_product_price(self):
        return "//p[@class='product-price']"

    def get_modal_page_name(self):
        return "//h4[@class='bold color-dorato']"

    def continue_button(self):
        return 'btn' and 'addedcart-btn' and 'pull-left'

    def back_to_shopping(self):
        return 'productBack'

    def shopping_bag_button(self):
        return 'btn' and 'addedcart-btn' and 'pull-right'

    def terms_and_conditions(self):
        return 'condizioni'

    def go_check_out(self):
        return "//a[@class='btn btn-lg pull-right']"

    def checkout_paypal(self):
        return "//button[@id='checkout_next' and @value='Prossimo']"

    def update_cart_btn(self):
        return "//button[@class='cart-update']"



class Plm(Company):

    def wait_for_hidden(self):
        return True

    def get_code(self):
        return True

    def pay_ship(self):
        return False

    def modal_page_code(self):
        return False

    def back_to_shop(self):
        return False


    def get_url(self):
        base_url = 'http://pierrelouismascia.com/shop/' #@dev:dev@ux.
        return base_url

    def get_products_name(self):
        return 'product-thumb__title'

    def get_product_code(self):
        path = "//div[@class='product-info__description']"

        return path

    def get_single_product_name(self):
        return "//h1[@class='product-info__title']"

    def get_single_product_price(self):
        return "//span[@class='price']"

    def get_modal_page_name(self):
        return "//div[@class='col-sm-8 addedcart__dataprod']/h5"

    def continue_button(self):
        return 'btn' and 'addedcart__btn' and 'addedcart__btn--continue'

    def back_to_shopping(self):
        return 'btn addedcart__btn addedcart__btn--continue'

    def shopping_bag_button(self):
        return 'btn' and 'addedcart__btn' and 'addedcart__btn--buy'

    def terms_and_conditions(self):
        return 'id_condizioni_vendita'

    def go_check_out(self):
        return "//a[@class='btn form-actions__btn--checkout pull-right']"

    def checkout_paypal(self):
        return "//button[@id='checkout_paypal' and @value='Pay now']"

    def update_cart_btn(self):
        return "//button[@class='btn-rotate cart__btn--update sliding sliding-update']"


#-----PER AVVIARE LE ISTANZE-----------------

site_to_test = {'tannerie' : Tannerie(), 'plm': Plm()}

site_choice = input('Scegli il sito: ')
site_choice = site_choice.lower()
quantity = input('quanti articoli vuoi comprare? ')
print('Grazie, ora inizio il test sul sito ' + site_choice.capitalize())
print('Ora del test: ' + strftime("%Y/%m/%d - %H:%M:%S", gmtime()))

site = site_to_test[site_choice]
