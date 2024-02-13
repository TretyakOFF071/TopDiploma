from django.contrib.auth.forms import UserCreationForm

from .models import User, Profile
from django import forms

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2')

class ProfileForm(forms.ModelForm):
    position = forms.CharField()
    birthday = forms.DateField(widget=forms.DateInput)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)

    class Meta:
        model = Profile
        fields = ('birthday', 'tel', 'avatar', 'position')