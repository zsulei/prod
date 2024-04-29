# your_app/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Cart  # Убедитесь, что импортировали модель Cart


@receiver(user_logged_in)
def merge_carts(sender, user, request, **kwargs):
    session_key = request.session.session_key
    if session_key:
        anonymous_cart = Cart.objects.filter(session_key=session_key).first()
        if anonymous_cart:
            user_cart, created = Cart.objects.get_or_create(user=user)
            for item in anonymous_cart.items.all():
                item.cart = user_cart
                item.save()
            anonymous_cart.delete()
