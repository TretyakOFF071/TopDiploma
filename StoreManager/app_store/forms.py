from django.contrib.auth.forms import UserCreationForm

from .models import User, Customer, GoodCart, Good
from django import forms
from django.core.validators import RegexValidator

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2')

class CustomerForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)
    phone = forms.CharField(max_length=11, validators=[
        RegexValidator(regex='^\\+?[0-9]{11}$', message='Некорректный формат номера телефона.')])

    class Meta:
        model = Customer
        fields = ('birthday', 'phone', 'avatar')



class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = '__all__'

class EditGoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['name', 'category', 'selling_price', 'purchase_price', 'description', 'image', 'quantity', 'provider', 'activity_flag']


class CartAddForm(forms.ModelForm):

    class Meta:
        model = GoodCart
        fields = ('good_num', )