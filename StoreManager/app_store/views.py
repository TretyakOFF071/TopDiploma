from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .forms import UserForm, ProfileForm, GoodForm, ProviderForm, GoodCategoryForm
from .models import Profile, Provider, Good, GoodCategory
from .serializers import ProviderSerializer, GoodSerializer


# Create your views here.

def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            birthday = profile_form.cleaned_data['birthday']
            phone = profile_form.cleaned_data['phone']
            profile = Profile.objects.create(
                user=user,
                birthday=birthday,
                phone=phone,
            )
            profile.save()

            username = user_form.cleaned_data['username']
            raw_password = user_form.cleaned_data['password1']
            auth_user = authenticate(username=username, password=raw_password)
            login(request, auth_user)
            return redirect('profile')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid fields')

    user_form = UserForm()
    profile_form = ProfileForm()
    return render(request, 'app_store/register.html', context={
        'user_form': user_form,
        'profile_form': profile_form
    })



class CustomLoginView(LoginView):
    template_name = 'app_store/login.html'
    next_page = 'profile'

    def form_valid(self, form):
        response = super(CustomLoginView, self).form_valid(form)
        return response


class CustomLogoutView(LogoutView):
    template_name = 'app_store/logout.html'
    next_page = 'register'

def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'app_store/profile.html', context={'profile': profile})


# ------------------------------------API----------------------------------------------------------------------------
CACHE_TIME = 60 * 60 * 2

class ProviderAPIView(APIView):

    def get(self, request):
        data = cache.get_or_set('providers_list', Provider.objects.all(), CACHE_TIME)
        return JsonResponse(ProviderSerializer(data, many=True).data, safe=False)

    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            cache.delete('providers_list')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderDetailAPI(APIView):

    def get(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        data = cache.get_or_set(f'provider_{pk}', provider, CACHE_TIME)
        return JsonResponse(ProviderSerializer(data).data, safe=False)

    def put(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        serializer = ProviderSerializer(provider, data=request.data)
        if serializer.is_valid():
            cache.delete(f'provider_{pk}')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoodAPIView(APIView):

    def get(self, request):
        data = cache.get_or_set('goods_list', Good.objects.all(), CACHE_TIME)
        return JsonResponse(GoodSerializer(data, many=True).data, safe=False)

    def post(self, request):
        serializer = GoodSerializer(data=request.data)
        if serializer.is_valid():
            cache.delete('goods_list')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodDetailAPI(APIView):

    def get(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        data = cache.get_or_set(f'good_{pk}', good, CACHE_TIME)
        return JsonResponse(GoodSerializer(data).data, safe=False)

    def put(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        serializer = GoodSerializer(good, data=request.data)
        if serializer.is_valid():
            cache.delete(f'good_{pk}')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------Views--------------------------------------------------------------

class ProviderListView(View):
    def get(self, request):
        providers = Provider.objects.all()
        categories = GoodCategory.objects.all()
        selected_category = request.GET.get('category')
        name_filter = request.GET.get('name')

        if selected_category:
            providers = providers.filter(categories__id=selected_category)

        if name_filter:
            providers = providers.filter(name__icontains=name_filter)

        form = ProviderForm()
        return render(request, 'app_store/providers_list.html', {
            'providers': providers,
            'form': form,
            'categories': categories,
            'selected_category': selected_category,
            'name_filter': name_filter,
        })

    def post(self, request):
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('providers_list')
        else:
            providers = Provider.objects.all()
            categories = GoodCategory.objects.all()
            return render(request, 'app_store/providers_list.html', {
                'providers': providers,
                'form': form,
                'categories': categories,
            })

def delete_provider(request, provider_id):
    provider = get_object_or_404(Provider, pk=provider_id)
    if request.method == 'POST':
        provider.delete()
    return redirect('providers_list')

def edit_provider(request, provider_id):
    provider = get_object_or_404(Provider, pk=provider_id)
    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('providers_list')
    else:
        form = ProviderForm(instance=provider)
    return render(request, 'app_store/edit_provider.html', {'form': form, 'provider': provider})


class GoodCategoryListView(View):
    def get(self, request):
        categories = GoodCategory.objects.all()
        form = GoodCategoryForm()
        return render(request, 'app_store/categories_list.html', {'categories': categories, 'form': form})

    def post(self, request):
        form = GoodCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories_list')
        else:
            categories = GoodCategory.objects.all()
            return render(request, 'app_store/categories_list.html', {'categories': categories, 'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(GoodCategory, pk=category_id)
    if request.method == 'POST':
        category.delete()
    return redirect('categories_list')


class GoodsListView(View):
    def get(self, request):
        goods = Good.objects.all()
        form = GoodForm()
        return render(request, 'app_store/goods_list.html', {'goods': goods, 'form': form})

    def post(self, request):
        form = GoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            goods = Good.objects.all()
        return render(request, 'app_store/goods_list.html', {'goods': goods, 'form': form})

def delete_good(request, good_id):
    good = get_object_or_404(Good, pk=good_id)
    if request.method == 'POST':
        good.delete()
    return redirect('goods_list')

def edit_good(request, good_id):
    good = get_object_or_404(Good, pk=good_id)
    if request.method == 'POST':
        form = GoodForm(request.POST, request.FILES, instance=good)
        if form.is_valid():
            form.save()
            return redirect('goods_list')
    else:
        form = GoodForm(instance=good)
    return render(request, 'app_store/edit_good.html', {'form': form, 'good': good})

