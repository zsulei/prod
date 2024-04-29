from django import forms

from .models import Product


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', ]
