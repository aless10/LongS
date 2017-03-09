'''
Dati di configurazione e avvio per il test su ecommerce
'''
import os
import sys
from time import gmtime, strftime, sleep

home_path = sys.prefix
chrome_pat = '/selenium/webdriver/chrome/chromedriver'
# percorso per caricare il chromedriver
path_to_chrome = home_path + chrome_pat
# dati account per acquisto con paypal
email = 'andrea.doppiozero-buyer@gmail.com'
password = 'Nonlaso00'


class Company(object):

    #ha il codice prodotto
    def get_code(self):
        return False
    # ha la modale quando clicco su acquista prodotto
    def is_modal(self):
        return True
    #il codice prodotto è presente nella modale
    def modal_page_code(self):
        return True

    def total_in_table(self):
        return False

    def back_to_shop(self):
        return True
    #spese di spedizione
    def pay_ship(self):
        return True
    #selezionare lo stato di fatturazione
    def select_state(self):
        return True
    #
    def return_to_terms_and_conditions(self):
        return True
    #al pagamento direttamente su paypal
    def road_to_paypal(self):
        return True
    
    #Attende che i campi si nascondano
    def wait_for_hidden_fields(self):
        return True

    #attendere che scelta quantità vengano nascosti
    def wait_for_hidden(self):
        hidden = ("//input[@type='hidden']",
                  "//input[@type='hidden']",
                  "//input[@id='id_quantity']",
                  "//select[@id='id_option2']",
                  )
        return hidden

    #stati e prezzi di spedizione
    def states(self):
        states = {'Austria': 15.0, 'Italia': 10.0, 'USA': 35.0}
        return states
    #cliccare e accettare i cookie
    def get_cookie(self):
        return "//a[@id='cookieChoiceDismiss']"

    def get_price(self):
        return "//span[@class='price']"

    def modal_id(self):
        return 'aggiuntoCarrello'

    def add_cart_btn(self):
        return "//button[@id='add_cart_btn']"

    def get_total_price(self):
        return "//div[@class='total']"

    def get_sub_total_price(self):
        return "//div[@class='order-totals']//div"

    def get_user_data(self):
        user_data = {
        'first_name': "id_billing_detail_first_name",
        'last_name': "id_billing_detail_last_name",
        'street': "id_billing_detail_street",
        'city': "id_billing_detail_city",
        'state': "id_billing_detail_state",
        'postcode': "id_billing_detail_postcode",
        'phone': "id_billing_detail_phone",
        'email': "id_billing_detail_email",
        'add_instruction': "id_additional_instructions",
        }
        return user_data

    def button_back_paypal(self):
        return "//button[@name='back']"

    def update_quantity(self):
        return "//input[@id='id_items-0-quantity']"

    def pay_pal_price(self):
        return "//span[@class='ltrOverride ng-binding']"

    def i_frame(self):
        iframe = ('iframe',
                  "//input[@placeholder='Indirizzo email']",
                  'password',
                  'btnLogin',
                  'confirmButtonTop',
                )
        return iframe


class Tannerie(Company):

    def road_to_paypal(self):
        return False

    def total_in_table(self):
        return True

    def get_url(self):
        base_url = 'http://dev:dev@ux.tannerie.doppiozero.to/it/donna/?cat%5B%5D=Borse+a+mano'
        return base_url

    def get_product_page_link(self):
        return "//h2[@class='box-title']"

    def get_products_name(self):
        return "//h2[@class='box-title']"

    def get_product_code(self):
        return "//p[@class='product-code']"

    def get_single_product_name(self):
        return "//h1[@class='product-title']"

    def get_single_product_price(self):
        return "//p[@class='product-price']"

    def get_modal_page_name(self):
        return "//h4[@class='bold color-dorato']"

    def before_code(self):
        return False

    def continue_button(self):
        return 'btn' and 'addedcart-btn' and 'pull-left'

    def back_to_shopping(self):
        return 'productBack'

    def shopping_bag_button(self):
        return 'btn' and 'addedcart-btn' and 'pull-right'

    def terms_and_conditions(self):
        return "//label[@class='checkbox-label newsletter-label']"

    def go_check_out(self):
        return "//a[@class='btn btn-lg pull-right']"

    def checkout_paypal(self):
        return "//button[@id='checkout_next' and @value='Prossimo']"

    def update_cart_btn(self):
        return "//button[@class='cart-update']"

    def complete_url(self):
        return 'http://ux.plm.doppiozero.to/shop/checkout/complete/'


class Volley(Company):

    def get_code(self):
        return True

    def pay_ship(self):
        return False

    def modal_page_code(self):
        return False

    def back_to_shop(self):
        return False

    def select_state(self):
        return False

    def states(self):
        states = ['Albania', 'Algeria']
        return states

    def get_url(self):
        base_url = 'http://dev:dev@ux.atleti.volleysport.it/shop/tutti-i-saldi/calzature-volley/'
        return base_url

    def get_product_page_link(self):
        return "//div[@class='info-prod']"

    def get_products_name(self):
        return "//div[@class='info-prod']/h5"

    def get_price(self):
        return "//span[@class='prezzo-prod-scontato']"

    def get_single_product_name(self):
        return "//h4[@class='titolo-prodotto']"

    def get_product_code(self):
        path = "//p[@class='smallinfo']"
        return path

    def get_single_product_price(self):
        return "//span[@class='prezzo-prodotto-scontato']"

    def get_modal_page_name(self):
        return "//div[@class='col-sm-8 aggiuntocarrello-datiprod']/h5"

    def before_code(self):
        return True

    def continue_button(self):
        return 'btn-back' and 'continua'

    def back_to_shopping(self):
        return 'btn addedcart__btn addedcart__btn--continue'

    def shopping_bag_button(self):
        return 'btn-salmon'

    def terms_and_conditions(self):
        return 'id_condizioni_vendita'

    def go_check_out(self):
        return "//a[@class='btn form-actions__btn--checkout pull-right']"

    def checkout_paypal(self):
        return "//button[@class='btn form-actions__btn--next pull-right']"

    def update_cart_btn(self):
        return "//button[@class='btn-rotate cart__btn--update sliding sliding-update']"


class Plm(Company):

    def wait_for_hidden(self):
        return False

    def get_code(self):
        return True

    def pay_ship(self):
        return False

    def modal_page_code(self):
        return False

    def back_to_shop(self):
        return False

    def select_state(self):
        return False

    def states(self):
        states = ['Albania', 'Algeria']
        return states

    def return_to_terms_and_conditions(self):
        return False

    def path_to_select_state(self):
        path = ('id_billing_detail_state_chosen',
                "//div[@class='chosen-search']/input[@type='text']",
                "//li[@class='active-result highlighted']",
                )
        return path

    def get_url(self):
        base_url = 'http://@dev:dev@ux.plm.doppiozero.to/shop/'
        return base_url

    def get_product_page_link(self):
        return "//h5[@class='product-thumb__title']"

    def get_products_name(self):
        return "//h5[@class='product-thumb__title']"

    def get_product_code(self):
        product_code = ("//div[@class='product-info__description']/label[@class='product-info__label']",
                        "//div[@class='product-info__description']", )
        return product_code

    def get_single_product_name(self):
        return "//h1[@class='product-info__title']"

    def get_single_product_price(self):
        return "//span[@class='price']"

    def get_modal_page_name(self):
        return "//div[@class='col-sm-8 addedcart__dataprod']/h5"

    def before_code(self):
        return True

    def continue_button(self):
        return 'btn' and 'addedcart__btn' and 'addedcart__btn--continue'

    def back_to_shopping(self):
        return 'btn addedcart__btn addedcart__btn--continue'

    def shopping_bag_button(self):
        return 'btn' and 'addedcart__btn' and 'addedcart__btn--buy'

    def terms_and_conditions(self):
        return "//label[@class='control-label' and @for='id_condizioni_vendita']"

    def button_back_paypal(self):
        return "//a[@class='userpanel__link userpanel__link--shopcart sliding']"

    def go_check_out(self):
        return "//a[@class='btn form-actions__btn--checkout pull-right']"

    def checkout_paypal(self):
        return "//button[@class='btn form-actions__btn--next pull-right']"

    def update_cart_btn(self):
        return "//button[@class='btn-rotate cart__btn--update sliding sliding-update']"

    def bnl_frame(self):
        bnl_to_paypal = ("//span[@class='value']",
                         "//input[@name='TARGET_TID']",
                         'document.getElementById("confirm").click();',
                        )
        return bnl_to_paypal

    def complete_url(self):
        return 'http://ux.plm.doppiozero.to/shop/checkout/complete/'


#-----PER AVVIARE LE ISTANZE-----------------

site_to_test = {'tannerie': Tannerie(), 'plm': Plm(), 'volley': Volley()}
print('Scegli il sito da testare tra quelli indicati')
for company in site_to_test.keys():
    print(company + '    ', end='\n')
site_choice = input('Scrivi il nome del sito')
site_choice = site_choice.lower()
num_elements_to_test = int(input('Quanti articoli vuoi comprare? '))
print('Grazie, ora inizio il test sul sito ' + site_choice.capitalize())
print('Ora del test: ' + strftime("%Y/%m/%d - %H:%M:%S", gmtime()))

site = site_to_test[site_choice]
