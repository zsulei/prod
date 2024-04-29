from django.contrib import admin

# Register your models here.
from .models import Category, Color, Material, Product, Size

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Material)
admin.site.register(Color)
admin.site.register(Size)
