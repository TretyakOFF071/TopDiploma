from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.forms import inlineformset_factory

from .models import User, Profile, Good, GoodCategory, Provider, Supply, Sale, SupplyGood, SaleItem
from django import forms
from django.utils.translation import gettext_lazy as _



class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 250px; margin: 0 auto;'}),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 250px; margin: 0 auto;'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': _('Имя пользователя'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Email'),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 250px; margin: 0 auto;'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 250px; margin: 0 auto;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 250px; margin: 0 auto;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 250px; margin: 0 auto;'}),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('birthday', 'phone', 'position')
        labels = {
            'birthday': _('Дата рождения'),
            'phone': _('Номер телефона'),
            'position': _('Должность')
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'form-control',
                                               'style': 'width: 250px; margin: 0 auto;'}),
            'phone': forms.TextInput(attrs={'class': 'form-control',
                                                           'style': 'width: 250px; margin: 0 auto;'}),
            'position': forms.TextInput(attrs={'class': 'form-control',
                                            'style': 'width: 250px; margin: 0 auto;'}),
        }
class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        exclude = ['sold_quantity', 'quantity']
        labels = {
            'name': _('Название товара'),
            'part_number': _('Артикул'),
            'category': _('Категория'),
            'selling_price': _('Цена продажи'),
            'purchase_price': _('Закупочная цена'),
            'description': _('Описание товара'),
            'image': _('Картинка товара'),
            'manufacturer': _('Производитель'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'style': 'width: 250px; margin: 0 auto;'}),
            'part_number': forms.TextInput(attrs={'class': 'form-control',
                                                  'style': 'width: 250px; margin: 0 auto;'}),
            'category': forms.Select(attrs={'class': 'form-select',
                                            'style': 'width: 250px; margin: 0 auto;'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control',
                                                      'style': 'width: 250px; margin: 0 auto;'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control',
                                                       'style': 'width: 250px; margin: 0 auto;'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'style': 'width: 250px; height: 50px; margin: 0 auto;'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control',
                                                     'style': 'width: 250px; margin: 0 auto;'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control',
                                            'style': 'width: 250px; margin: 0 auto;'}),
        }


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'contact_person', 'phone_number', 'email', 'categories']
        labels = {
            'name': _('Название поставщика'),
            'contact_person': _('Контактное лицо'),
            'phone_number': _('Номер телефона'),
            'email': _('Электронная почта'),
            'categories': _('Категории товаров'),
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
            'categories': forms.SelectMultiple(attrs={'class': 'form-select',
                                                      'style': 'width: 250px; margin: 0 auto;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = GoodCategory.objects.all()

class GoodCategoryForm(forms.ModelForm):
    class Meta:
        model = GoodCategory
        fields = ['name']
        labels = {
            'name': _('Категория товара')
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                        'style': 'width: 200px; margin: 0 auto;'})
        }

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['provider']
        labels = {
            'provider': _('Поставщик')
        }
        widgets = {
            'provider': forms.Select(attrs={'class': 'form-select',
                                            'style': 'width: 250px; margin: 0 auto;'})
        }

class SupplyGoodForm(forms.ModelForm):
    class Meta:
        model = SupplyGood
        fields = ['good', 'quantity']
        labels = {
            'good': _('Товар'),
            'quantity': _('Количество товаров')
        }
        widgets = {
            'good': forms.Select(attrs={'class': 'form-select',
                                        'style': 'width: 250px; margin: 0 auto;'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control',
                                                 'style': 'width: 250px; margin: 0 auto;'}),
        }

SupplyGoodFormSet = inlineformset_factory(Supply, SupplyGood, form=SupplyGoodForm, extra=5, can_delete=False)

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['discount', 'payment_method']
        labels = {
            'discount': _('Скидка'),
            'payment_method': _('Способ оплаты')
        }
        widgets = {
            'discount': forms.NumberInput(attrs={'class': 'form-control',
                                                 'step': 1,
                                                 'style': 'width: 250px; margin: 0 auto;', 'min': 0, 'max': 50, 'max_length': 3}),
            'payment_method' : forms.Select(attrs={'class': 'form-select', 'style': 'width: 250px; margin: 0 auto;'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['discount'].validators = [MinValueValidator(0), MaxValueValidator(50), MaxLengthValidator(2)]


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['good', 'quantity']
        labels = {
            'good': _('Товар'),
            'quantity': _('Количество')
        }
        widgets = {
            'good': forms.Select(attrs={'class': 'form-select', 'style': 'width: 250px;  margin: 0 auto;'}),
            'quantity': forms.NumberInput(attrs={'max_length': 2, 'class': 'form-control', 'style': 'width: 250px; margin: 0 auto;'}),
        }


SaleItemFormSet = inlineformset_factory(Sale, SaleItem, form=SaleItemForm, extra=3, can_delete=False)