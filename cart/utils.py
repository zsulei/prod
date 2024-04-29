
from .models import Cart


def cart_checker(request):
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session_key=session_key, defaults={'user': None})
    return cart


def cart_total_price(cart):
    total = 0
    for item in cart.items.all():
        total += item.product.price * item.quantity
    return total
