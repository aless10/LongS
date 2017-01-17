import re

#FUNZIONE AUSILIARIA CHE MI PERMETTE DI CONVERTIRE I PREZZI IN NUMERI COSI' POSSO FARE I CALCOLI
def price_converter(price):
    '''
    :param price: string
    :return: float price
    '''
    price = list(price)
    price.remove('€')
    price.remove(' ')
    price.remove(',')
    if '.' in price:
        price.remove('.')
    price.insert(-2, '.')
    price = float(''.join(price))
    return price

# IN shop/checkout/
# def slice_prod_name(prod_name):
#     list_prod = list(prod_name)
#     list_prod.remove(' ')
#     index_stop =
#     name = list_prod[]