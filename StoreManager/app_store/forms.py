from django.contrib.auth.forms import UserCreationForm

from .models import User, Profile, Good, GoodCategory, Provider
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
        exclude = ['sold_quantity']


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'contact_person', 'phone_number', 'email', 'categories']
class GoodCategoryForm(forms.ModelForm):
    class Meta:
        model = GoodCategory
        fields = ['name']