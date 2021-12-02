from django import template
from shop.models.shops import Shop

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product  , session):
    cart = session.get('cart')
    if cart:
        keys = cart.keys()
        for id in keys:
            if int(id) == product.id:
                return True
    return False;

@register.filter(name='cart_quantity')
def cart_quantity(product  , session):
    cart = session.get('cart')
    if cart:
        keys = cart.keys()
        for id in keys:
            if int(id) == product.id:
                return cart.get(id)
    return 0;

@register.filter(name='total_cart_quantity')
def total_cart_quantity(user, session):
    cart = session.get('cart')
    if cart:
        return sum(cart.values())
    return 0

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price

@register.simple_tag()
def addition(total, qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    val = qty * unit_price
    return val+total

@register.filter(name='total_shops')
def total_shops(user, request):
    return len(Shop.objects.all())

