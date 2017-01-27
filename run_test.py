'''
FILE DA UTILIZZARE PER LANCIARE LA SUITE DI TEST
ALL'INIZIO CHIEDE IL NOME DEL SITO DA TESTARE (AZIENDA) E QUANTI PRODOTTI SI VUOLE COMPRARE
'''

from GitHub.test_checkout.test_shop import BuyAProductTest
import unittest

buy_product_tests = unittest.TestLoader().loadTestsFromTestCase(BuyAProductTest)

smoke_tests = unittest.TestSuite([buy_product_tests])
# run the suite
unittest.TextTestRunner(verbosity=2).run(smoke_tests)
