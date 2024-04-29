from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from cart.forms import AddToCartForm
from cart.utils import cart_checker, cart_total_price
import random
from .forms import ProductImageForm
from .models import Category, Product, Size
from .utils import start_func


class IndexView(TemplateView):
    template_name = 'products/index.html'
    title = 'Outlet Obuv'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Store'


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 15
    title = 'Outlet obuv - Каталог'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        queryset = queryset.filter(is_hidden=False)
        category_id = self.kwargs.get('pk')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **krwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    form = AddToCartForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        product_color = self.object.color
        product_material = self.object.material
        context['material'] = product_material
        context['color'] = product_color
        cart = cart_checker(self.request)
        context['cart'] = cart
        total = cart_total_price(cart)
        context['total'] = total
        context['image_form'] = ProductImageForm
        similar = Product.objects.filter(category=product.category)
        same_category = random.sample(list(similar), 4)
        context['similar_products'] = same_category
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductImageForm
    template_name = 'products/update_product.html'
    success_url = reverse_lazy('update_product_image')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.image = self.request.FILES['image']
        product.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.object.pk})


def get_colors_sizes(request):
    material_id = request.GET.get('material_id')
    if material_id:
        sizes = Size.objects.filter(material_id=material_id).select_related('color')
        size_color_data = {
            'sizes': list(sizes.values_list('value', flat=True).distinct()),
            'colors': list(sizes.values_list('color__name', flat=True).distinct())
        }
        return JsonResponse(size_color_data)
    else:
        return JsonResponse({'error': 'No material id provided'}, status=400)


def search_by_name(request):    # ДОДЕЛАТЬ
    query_data = request.GET.get('search_holder')
    query_article = Product.objects.filter(article__icontains=query_data)
    query_name = Product.objects.filter(name__icontains=query_data)
    query_size = Size.objects.filter(product__article__icontains=query_article)
    queryset = query_article | query_name
    categories = Category.objects.all()

    context = {
        'products': queryset,
        'categories': categories,
        'sizes': query_size
    }

    return render(request, 'products/search.html', context)


def about(request):  # ДОДЕЛАТЬ
    return render(request, 'products/about.html')


def parse_tsgoods_view(request):
    file_path = 'C:/Users/2021/Desktop/udemy/outletobuv_core/TSGoods.trs'

    try:
        start_func(file_path)
        # hide_products()
        return HttpResponse("File parsed successfully.")
    except Exception as e:
        print(e)
        return HttpResponse(f"Error occurred: {e}")


def delete_all(request):
    Product.objects.all().delete()
    Category.objects.all().delete()
    Size.objects.all().delete()
    print('Все объекты удалены')
    return redirect('products:index')


def get_sizes(request):
    material_name = request.GET.get('materialName')
    color_name = request.GET.get('colorName')
    sizes = (Size.objects.filter(material__name=material_name, color__name=color_name)
             .values_list('id', 'value', named=True))
    unique_sizes = {}
    for size in sizes:
        if size.value not in unique_sizes:
            unique_sizes[size.value] = size.id
    sizes_json = [{'id': unique_sizes[value], 'value': value} for value in unique_sizes]
    return JsonResponse(sizes_json, safe=False)


def products2(request, category_id=None, page_number=1):    # Проверка товаров
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    per_page = 15
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)
    categories = Category.objects.all()
    context = {
        'title': 'Outlet Obuv',
        'categories': categories,
        'products': products_paginator,
    }
    return render(request, 'products/products2.html', context)


def strange_products(request):  # ДОДЕЛАТЬ
    products_without_color_or_material = Product.objects.filter(color__isnull=True)

    context = {
        'products': products_without_color_or_material
    }
    print(products_without_color_or_material)
    return render(request, 'products/strange.html', context)
