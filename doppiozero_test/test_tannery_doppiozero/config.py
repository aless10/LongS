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

    def get_cookie(self):
        self.cookie = "//a[@id='cookieChoiceDismiss']"
        return self.cookie


base_url = 'http://dev:dev@ux.tannerie.doppiozero.to/it/donna/?cat%5B%5D=Borse+a+mano'
