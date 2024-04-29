from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('rm_from_cart/<int:product_id>/<int:material_id>/<int:color_id>/<int:size_id>/',
         views.rm_from_cart, name='rm_from_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('order-create/', views.create_order, name='order_create'),
    path('done/', views.done, name='done')
]
