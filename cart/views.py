import requests
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .forms import AddToCartForm, OrderForm
from .models import Cart, CartItem, OrderItem
from .utils import cart_checker


def add_to_cart(request, product_id):
    session_key = request.session.session_key
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = AddToCartForm(request.POST, product_id=product_id,
                             material_id=request.POST.get('material'),
                             color_id=request.POST.get('color')
                             )
        if form.is_valid():
            material = form.cleaned_data['material']
            color = form.cleaned_data['color']
            size = form.cleaned_data['size']
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                material=material,
                color=color,
                size=size,
                defaults={'quantity': 1}
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return redirect(request.META['HTTP_REFERER'])
        else:
            print(form.errors)

        return render(request, 'products/product.html', {'form': form, 'product': product})


def rm_from_cart(request, product_id, material_id, color_id, size_id):
    session_key = request.session.session_key
    # product = get_object_or_404(Product, product_id)
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    try:
        if request.method == 'POST':
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id,
                                                material_id=material_id, color_id=color_id,
                                                size_id=size_id)
            cart_item.delete()
        return redirect(request.META['HTTP_REFERER'])
    except Exception as e:
        return HttpResponse(str(e))  # Adjusted to return a valid HttpResponse


def cart_detail(request):
    cart = cart_checker(request)
    total = 0
    for item in cart.items.all():
        total += item.product.price
    print(total)
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'total': total})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['first_name'], form.cleaned_data['phone_number'])
            order = form.save(commit=False)
            order.save()
            cart = Cart.objects.get(session_key=request.session.session_key)
            number = form.cleaned_data['phone_number']
            number = number.strip().replace('+', '').replace(' ', '').replace('-', '')

            message = [f'Заказ для клиента {form.cleaned_data["first_name"]} ',
                       'http://wa.me/' + number]
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    size=item.size,
                    color=item.color,
                    material=item.material
                )
                print(item)
                message.append((item.product.article, item.size.value, item.color.name, item.material.name))

            cart.items.all().delete()

            messages.success(request, 'Ваш заказ успешно оформлен!')
            token = '6364051759:AAH0QqDgl16iPg_NfJHTDe75PtbeN3jYA_E'
            chat_id = '303438120'
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
            requests.get(url)
            return redirect('cart:done')
        else:
            return render(request, 'cart/order-create.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'cart/order-create.html', {'form': form})


def done(request):
    return render(request, 'cart/done.html')
