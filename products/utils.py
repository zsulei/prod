import csv
from time import time

from .models import Category, Color, Material, Product, Size

'''
"Articul";"GoodTypeFull";"Category";
"WarehouseQuantity";"Material";"GoodName";
"PCName";"TheSize";"Season";
"PriceDiscountPercent";"Color";"RetailPrice"
'''


def time_decor(function):
    def wrapper(*args, **kwargs):
        start_time = time()
        func = function(*args, **kwargs)
        end_time = time()
        print(f'Время выполнения функции {func}: ', start_time - end_time)
        return func
    return wrapper


@time_decor
def start_func(file_path):
    hide_products()
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # with transaction.atomic():
            create_product(row)


@time_decor
def create_product(row):
    try:
        category_title = row['GoodTypeFull'].replace('Обувь,', '').strip()
        category, _ = Category.objects.get_or_create(title=category_title)
        product, created = Product.objects.get_or_create(
            article=row['Articul'],
            defaults={
                'name': row['GoodName'].split()[0],
                'category': category,
                'season': row['Season'],
                'price': row['RetailPrice'],
                'quantity': row['WarehouseQuantity']
            }
        )

        color, _ = Color.objects.get_or_create(name=row['Color'])
        material, _ = Material.objects.get_or_create(name=row['Material'])

        product.color.add(color)
        product.material.add(material)
        product.is_hidden = False
        product.save()

        size, created = Size.objects.get_or_create(
            value=row['TheSize'],
            product=product,
            color=color,
            material=material
        )

        if created:
            product.is_hidden = False
            product.save()
    except Exception as e:
        print(f'Произошла ошибка: {e}')


@time_decor
def hide_products():
    try:
        Product.objects.all().update(is_hidden=True)
        print('Products hide')
    except Exception as e:
        products = Product.objects.all()
        for product in products:
            product.is_hidden = True
            print(e)


def handle_uploaded_file(f):
    with open("1.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
