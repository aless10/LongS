'''
Dati di configurazione e avvio per il test su tannery
'''

# percorso per caricare il chromedriver
path_to_chrome = '/home/ale/VirtuaPyCharm/bin/chrome/chromedriver'
num_elements_to_test = 2
email = 'andrea.doppiozero-buyer@gmail.com'
password = 'Nonlaso00'
states = {'Austria': 15.0, 'Italia': 10.0, 'USA': 35.0}
site_to_test = ['tannerie', 'plm', ]


class Tannerie():

    def get_url(self):
        base_url = 'http://dev:dev@ux.tannerie.doppiozero.to/it/donna/?cat%5B%5D=Borse+a+mano'
        return base_url

    def get_cookie(self):
        self.cookie = "//a[@id='cookieChoiceDismiss']"
        return self.cookie

    def get_products_name(self):
        return "box-title"

    def get_price(self):
        return "//span[@class='price']"

    def get_single_product_name(self):
        return "//h1[@class='product-title']"

    def get_single_product_price(self):
        return "//p[@class='product-price']"

    def get_modal_page_name(self):
        return "//h4[@class='bold color-dorato']"

    def continue_button(self):
        return 'btn' and 'addedcart-btn' and 'pull-left'

    def shopping_bag_button(self):
        return 'btn' and 'addedcart-btn' and 'pull-right'

    def terms_and_conditions(self):
        return 'condizioni'

class Plm():

    def get_url(self):
        base_url = 'http://dev:dev@ux.plm.doppiozero.to/shop/'
        return base_url

    def get_cookie(self):
        self.cookie = "//a[@id='cookieChoiceDismiss']"
        return self.cookie

    def get_products_name(self):
        return 'product-thumb__title'

    def get_price(self):
        return "//span[@class='price']"

    def get_single_product_name(self):
        return "//h1[@class='product-info__title']"

    def get_single_product_price(self):
        return "//span[@class='price']"

    def get_modal_page_price(self):
        return "h5"

    def continue_button(self):
        return 'btn' and 'addedcart__btn' and 'addedcart__btn--continue'

    def shopping_bag_button(self):
        return 'btn' and 'addedcart__btn' and 'addedcart__btn--buy'

    def terms_and_conditions(self):
        return 'id_condizioni_vendita'