from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from .models import User, Profile, Good, GoodCategory, Provider, Supply, SupplyItem
from django import forms
from django.core.validators import RegexValidator

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2')

class ProfileForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput)
    phone = forms.CharField(max_length=11, validators=[
        RegexValidator(regex='^\\+?[0-9]{11}$', message='Некорректный формат номера телефона.')])

    class Meta:
        model = Profile
        fields = ('birthday', 'phone')



class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        exclude = ['sold_quantity', 'quantity', 'activity_flag']
        labels = {
            'name': 'Название товара',
            'part_number': 'Артикул',
            'category': 'Категория',
            'selling_price': 'Цена продажи',
            'purchase_price': 'Закупочная цена',
            'description': 'Описание товара',
            'image': 'Картинка товара',
            'provider': 'Поставщик',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'style': 'width: 250px; margin: 0 auto;'}),
            'part_number': forms.TextInput(attrs={'class': 'form-control',
                                                  'style': 'width: 250px; margin: 0 auto;'}),
            'category': forms.Select(attrs={'class': 'form-control',
                                            'style': 'width: 250px; margin: 0 auto;'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control',
                                                      'style': 'width: 250px; margin: 0 auto;'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control',
                                                       'style': 'width: 250px; margin: 0 auto;'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'style': 'width: 250px; height: 50px; margin: 0 auto;'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control',
                                                     'style': 'width: 250px; margin: 0 auto;'}),
            'provider': forms.Select(attrs={'class': 'form-control',
                                            'style': 'width: 250px; margin: 0 auto;'}),
        }


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'contact_person', 'phone_number', 'email', 'categories']
        labels = {
            'name': 'Название поставщика',
            'contact_person': 'Контактное лицо',
            'phone_number': 'Номер телефона',
            'email': 'Электронная почта',
            'categories': 'Категории товаров',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'style': 'width: 250px; margin: 0 auto;'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control',
                                                     'style': 'width: 250px; margin: 0 auto;'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control',
                                                   'style': 'width: 250px; margin: 0 auto;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'style': 'width: 250px; margin: 0 auto;'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control',
                                                      'style': 'width: 250px; margin: 0 auto;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = GoodCategory.objects.all()

class GoodCategoryForm(forms.ModelForm):
    class Meta:
        model = GoodCategory
        fields = ['name']



class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['provider']
        labels = {
            'provider': 'Поставщик'
        }
        widgets = {
            'provider': forms.Select(attrs={'class': 'form-control',
                                            'style': 'width: 250px; margin: 0 auto;'}),
        }

class SupplyItemForm(forms.ModelForm):
    class Meta:
        model = SupplyItem
        fields = ['good', 'quantity']
        labels = {
            'good': 'Товар',
            'quantity': 'Количество товаров'
        }
        widgets = {
            'good': forms.Select(attrs={'class': 'form-control',
                                        'style': 'width: 250px; margin: 0 auto;'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control',
                                                 'style': 'width: 250px; margin: 0 auto;'}),
        }

SupplyItemFormSet = inlineformset_factory(Supply, SupplyItem, form=SupplyItemForm, extra=1, can_delete=False)