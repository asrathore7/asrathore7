'''Contain functionality of cart.'''
from django import template
from shop.models.shops import Shop

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, session):
    '''is in cart to check product is available or not in cart'''
    cart = session.get('cart')
    if cart:
        keys = cart.keys()
        for key in keys:
            if int(key) == product.id:
                return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(product, session):
    '''get total quantity into cart of product'''
    cart = session.get('cart')
    if cart:
        keys = cart.keys()
        for key in keys:
            if int(key) == product.id:
                return cart.get(key)
    return 0

@register.filter(name='total_cart_quantity')
def total_cart_quantity(user, session):
    '''get total quantity into cart'''
    print(user)
    cart = session.get('cart')
    if cart:
        return sum(cart.values())
    return 0

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    '''return subtotal of product.'''
    print(kwargs, args)
    return qty * unit_price

@register.simple_tag()
def addition(total, qty, unit_price, *args, **kwargs):
    '''Count total of all orderline.'''
    print(kwargs, args)
    val = qty * unit_price
    return val+total

@register.filter(name='total_shops')
def total_shops(user, request):
    '''Count all shop'''
    print(user, request)
    return len(Shop.objects.all())
