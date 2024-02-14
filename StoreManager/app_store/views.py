from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView

from .forms import UserForm, CustomerForm, CartAddForm, GoodForm
from .models import Customer, Good
from django.contrib import messages


class UserUpdateView(UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'app_shop/profile.html'


    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})


class MainView(ListView):

    model = Good
    queryset = Good.objects.select_related('category').defer('quantity', 'activity_flag'
                                                                     ).filter(quantity__gt=0, activity_flag='a')
    context_object_name = 'goods'
    template_name = 'app_store/main.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['avg_price'] = Good.objects.only('selling_price').aggregate(avg_price=Avg('selling_price')).get('avg_price')
        context['add_form'] = CartAddForm()
        return context

def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_dorm = CustomerForm(request.POST, request.FILES)

        if user_form.is_valid() and customer_dorm.is_valid():
            user = user_form.save()
            birthday = customer_dorm.cleaned_data['birthday']
            phone = customer_dorm.cleaned_data['phone']
            avatar = customer_dorm.cleaned_data['avatar']
            customer = Customer.objects.create(
                user=user,
                birthday=birthday,
                phone=phone,
                avatar=avatar
            )
            customer.save()

            username = user_form.cleaned_data['username']
            raw_password = user_form.cleaned_data['password1']
            auth_user = authenticate(username=username, password=raw_password)
            login(request, auth_user)
            return redirect('main')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid fields')

    user_form = UserForm()
    customer_dorm = CustomerForm()
    return render(request, 'app_store/register.html', context={
        'user_form': user_form,
        'customer_form': customer_dorm
    })


class CustomLoginView(LoginView):
    template_name = 'app_store/login.html'
    next_page = 'main'

    def form_valid(self, form):
        response = super(CustomLoginView, self).form_valid(form)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('main')



def profile_view(request):
    profile = get_object_or_404(Customer, user=request.user)
    return render(request, 'app_store/profile.html', context={'profile': profile})


class GoodListView(ListView):
    model = Good
    template_name = 'good_list.html'  # Путь к вашему шаблону
    context_object_name = 'goods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['good_form'] = GoodForm()
        return context

def add_good(request):
    if request.method == 'POST':
        form = GoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно добавлен.')
            return redirect('good_list')  # Замените 'good_list' на имя вашего шаблона списка товаров
    else:
        form = GoodForm()
    return render(request, 'app_store/add_good.html', {'form': form})


