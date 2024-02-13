from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from .forms import UserForm, ProfileForm
from .models import Profile
from django.contrib import messages



def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            birthday = profile_form.cleaned_data['birthday']
            tel = profile_form.cleaned_data['tel']
            avatar = profile_form.cleaned_data['avatar']
            position = profile_form.cleaned_data['position']
            profile = Profile.objects.create(
                user=user,
                birthday=birthday,
                tel=tel,
                position=position,
                avatar=avatar
            )
            profile.save()

            username = user_form.cleaned_data['username']
            raw_password = user_form.cleaned_data['password1']
            auth_user = authenticate(username=username, password=raw_password)
            login(request, auth_user)
            return redirect('main')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid fields')


    user_form = UserForm()
    profile_form = ProfileForm()
    return  render(request, 'app_store/register.html', context={
        'user_form':  user_form,
        'profile_form': profile_form
    })

class CustomLoginView(LoginView):
    template_name = 'app_store/login.html'
    next_page = 'main'

    def form_valid(self, form):
        response = super(CustomLoginView, self).form_valid(form)
        return response

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('main')

def main_view(request, *args, **kwargs):
    profile = Profile.objects.all()
    return render(request, 'app_store/base.html', context={'profile': profile})

def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'app_store/profile.html', context={'profile': profile})