from django.db import models

from products.models import Color, Material, Product, Size
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=300, null=True, blank=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey('products.Material', on_delete=models.CASCADE)
    color = models.ForeignKey('products.Color', on_delete=models.CASCADE)
    size = models.ForeignKey('products.Size', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=13)
    address = models.CharField(max_length=255)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='order')

    def __str__(self):
        return f'Заказ # {self.id}. {self.first_name} {self.last_name} {self.phone_number}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order.id} - {self.product.name}'
