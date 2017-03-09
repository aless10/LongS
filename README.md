# test-checkout

Doppiozero - Test

Guida all'utilizzo della suite di test per ecommerce Doppiozero

0. Creazione ambiente virtuale
   >> virtualenv venvtest
   
   >> source venvtest/bin/activate

1. Installazione Selenium WebDriver:
   >> pip install -U selenium

2. Download repository da Github
   https://github.com/unbit-is/test-checkout/

3. Avvio suite di test:
   >> python run_test.py
   Viene mostrata la scelta tra i possibili siti da testare. Occorre digitare il nome del sito (tra quelli dell'elenco).
   E' necessario scegliere quanti prodotti comprare (>=1). Una volta premuto invio, si avvia il test.

4. Descrizione del test
   L'obiettivo del test è verificare il corretto funzionamento di un sito in seguito a una modifica (frontend o backend). Durante  ogni test viene simulato un flusso utente completo, dalla scelta del prodotto fino al completamento del pagamento (con paypal).

5. Risultati del test
   (Ovviamente) il test può avere due possibili esiti:
   a. il test è positivo -> non vengono rilevati errori
   b. il test è negativo -> durante la navigazione simulata, uno o più parametri non corrispondono con quelli attesi. Il test si ferma, viene salvato uno screenshot della pagina in cui si è verificato l'errore e viene mandata una mail con descrizione del 
 problema occorso e storia del flusso utente.

6. Descrizione del flusso utente
   Il test inizia con la selezione casuale di un prodotto, l'aggiunta al carrello e l'eventuale selezione di altri prodotti (in caso si scelga di compare più di un prodotto) che verranno inseriti nel carrello. Poi si passa all'inserimento dei dati di acquisto.
   Ritorno al carrello e update della quantità (+1) del primo prodotto messo in carrello. Si passa al checkout e poi al pagamento con Paypal. Vengono inseriti i dati e si procede al pagamento.

7. Cosa viene testato
   In ogni pagina, viene fatto un check sui dati dei prodotti da acquistare (nome, prezzo, codice)#DA AGGIUNGERE IL CHECK SULL'IMMAGINE
   Dal carrello in poi viene controllato che il prezzo singolo*quantità corrisponda con il totale di spedizione. Vengono anche aggiunte
   e controllate le spese di spedizione (dove previste).
