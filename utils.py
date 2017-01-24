import re

#FUNZIONE AUSILIARIA CHE MI PERMETTE DI CONVERTIRE I PREZZI IN NUMERI COSI' POSSO FARE I CALCOLI
def price_converter(price):
    '''
    :param price: string
    :return: float price
    '''
    price = list(price)
    if '€' in price:
        price.remove('€')
    price.remove(' ')
    if ',' in price:
        price.remove(',')
    if '.' in price:
        price.remove('.')
    price.insert(-2, '.')
    price = float(''.join(price))
    return price

# Funzione per salvare solo il codice
def slice_code(code):
    code_only = code.split(': ')
    code_only = code_only[1]
    return code_only

# Funzione per salvare il nome prodotto nel riepilogo
def slice_prod_name(name):
    product_name = name.split(' Colore')[0]
    return product_name

#Funzione per salvare solo il prezzo
def slice_prod_price(price):
    product_price = price.split('€ ')[1]
    product_price = '€ ' + product_price
    return product_price


def check_products_prizes(test, driver, products_info):
    cart_table = driver.find_element_by_xpath("//tbody")
    cart_rows = cart_table.find_elements_by_tag_name('tr')
    cart_rows.pop()
    total_price = 0
    n = 0
    for row in cart_rows:
        shopping_bag_prod = row.find_elements_by_tag_name('td')[1]
        shopping_bag_name = shopping_bag_prod.find_element_by_xpath("//strong").text
        #print(shopping_bag_name, n)
        test.assertEqual(shopping_bag_name, products_info['product ' + str(n)]['name'])
        shopping_bag_code = slice_code(\
            shopping_bag_prod.find_elements_by_xpath("//span[@class='cart-details']")[1].text)
        #print(shopping_bag_prod, n)
        # TEST CODICE PRODOTTO
        test.assertEqual(shopping_bag_code, products_info['product ' + str(n)]['code'])
        shopping_bag_price_1 = row.find_elements_by_tag_name('td')[2].text
        shopping_bag_price = price_converter(shopping_bag_price_1)
        #print(shopping_bag_price)
        test.assertEqual(shopping_bag_price, products_info['product ' + str(n)]['price'])
        quantity = row.find_elements_by_tag_name('td')[3]
        shopping_bag_quantity = int(quantity.find_element_by_tag_name('input').get_attribute('value'))
        shopping_bag_total_price = row.find_elements_by_tag_name('td')[4].text
        price_to_check = price_converter(shopping_bag_total_price)
        # CHECK SU PREZZO UNITARIO * QUANTITA' = PREZZO TOTALE
        test.assertEqual(price_to_check, shopping_bag_price * shopping_bag_quantity)
        total_price += price_to_check
        n += 1
    return total_price


def check_out_total_func(driver):
    product_list = driver.find_elements_by_xpath("//li[@class='media']")
    check_out_total = 0
    for product in product_list:
        # resume_div_name = slice_prod_name(product.text)
        resume_div_price = price_converter(slice_prod_price(product.text))
        check_out_total += resume_div_price
    return check_out_total
