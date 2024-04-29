from django import forms

from cart.models import Order
from products.models import Color, Material, Size


class AddToCartForm(forms.Form):
    color = forms.ModelChoiceField(widget=forms.Select, queryset=Color.objects.all(),
                                   empty_label='Выберите цвет', required=True)
    material = forms.ModelChoiceField(widget=forms.Select, queryset=Material.objects.all(),
                                      empty_label='Выберите материал', required=True)
    size = forms.ModelChoiceField(widget=forms.Select, queryset=Size.objects.all(),
                                  empty_label='Выберите размер', required=True)

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        material_id = kwargs.pop('material_id', None)
        color_id = kwargs.pop('color_id', None)
        super().__init__(*args, **kwargs)

        if material_id and color_id:
            self.fields['size'].queryset = Size.objects.filter(material_id=material_id, color_id=color_id)

    def clean_size(self):
        size = self.cleaned_data.get('size')
        material = self.cleaned_data.get('material')
        color = self.cleaned_data.get('color')
        if size not in Size.objects.filter(material=material, color=color):
            raise forms.ValidationError("Выбранный размер недоступен для данного материала и цвета.")
        return size


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ivan'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ivanov'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'name@example.com'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7'}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Укажите, куда доставить вашу посылку'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address')
