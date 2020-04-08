# LongS checkouter

0. Creazione ambiente virtuale
   >> virtualenv venv
   
   >> source venvtest/bin/activate

1. Installazione Selenium WebDriver:
   >> pip install -U selenium

2. Download repository da Github
   https://github.com/unbit-is/test-checkout/

3. Avvio suite di test:
   >> python run_test.py
   Viene mostrata la scelta tra i possibili siti da testare. Occorre digitare il nome del sito (tra quelli dell'elenco).
   E' necessario scegliere quanti prodotti comprare (>=1). Una volta premuto invio, si avvia il test.
